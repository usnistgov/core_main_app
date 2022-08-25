""" Ajax API
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template import loader
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import View

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_main_app.components.data import api as data_api
from core_main_app.components.group import api as group_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.templatetags.xsl_transform_tag import render_xml_as_html
from core_main_app.utils import group as group_utils
from core_main_app.views.user.forms import (
    ChangeWorkspaceForm,
    UserRightForm,
    GroupRightForm,
)

GROUP = "group"
USER = "user"

ACTION_READ = "action_read"
ACTION_WRITE = "action_write"


@method_decorator(login_required, name="dispatch")
class LoadFormChangeWorkspace(View):
    """Load the form to list the workspaces."""

    show_global_workspace = True

    def post(self, request, *args, **kwargs):
        """post

        Args:
             request:

        Returns:

        """

        is_administration = request.POST.get("administration", False) == "True"

        try:
            form = ChangeWorkspaceForm(
                request.user, list(), is_administration, self.show_global_workspace
            )
        except DoesNotExist as dne:
            return HttpResponseBadRequest(escape(str(dne)))
        except Exception:
            return HttpResponseBadRequest("Something wrong happened.")

        context = {"assign_workspace_form": form}

        return HttpResponse(
            json.dumps(
                {
                    "form": loader.render_to_string(
                        "core_main_app/user/workspaces/list/modals/assign_workspace_form.html",
                        context,
                    )
                }
            ),
            "application/javascript",
        )


@login_required
def load_add_user_form(request):
    """Load the form to list the users with no access to the workspace.

    Args:
        request:

    Returns:
    """
    workspace_id = request.POST.get("workspace_id", None)
    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
    except exceptions.ModelError:
        return HttpResponseBadRequest("Invalid input.")
    except Exception:
        return HttpResponseBadRequest("An unexpected error occurred.")

    try:
        # We retrieve all users with no access
        users_with_no_access = list(
            workspace_api.get_list_user_with_no_access_workspace(
                workspace, request.user
            )
        )

        # We remove the owner of the workspace
        if len(users_with_no_access) > 0:
            users_with_no_access.remove(user_api.get_user_by_id(workspace.owner))

        if len(users_with_no_access) == 0:
            return HttpResponseBadRequest("There is no users that can be added.")

        form = UserRightForm(users_with_no_access)
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    context = {"add_user_form": form}

    return HttpResponse(
        json.dumps(
            {
                "form": loader.render_to_string(
                    "core_main_app/user/workspaces/list/modals/add_user_form.html",
                    context,
                )
            }
        ),
        "application/javascript",
    )


@login_required
def add_user_right_to_workspace(request):
    """Add rights to user for the workspace.

    Args:
        request

    Returns
    """
    workspace_id = request.POST.get("workspace_id", None)
    users_ids = request.POST.getlist("users_id[]", [])
    is_read_checked = request.POST.get("read", None) == "true"
    is_write_checked = request.POST.get("write", None) == "true"

    if len(users_ids) == 0:
        return HttpResponseBadRequest("You need to select at least one user.")
    if not is_read_checked and not is_write_checked:
        return HttpResponseBadRequest(
            "You need to select at least one permission (read and/or write)."
        )

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
        for user in user_api.get_all_users_by_list_id(users_ids):
            if is_read_checked:
                workspace_api.add_user_read_access_to_workspace(
                    workspace, user, request.user
                )
            if is_write_checked:
                workspace_api.add_user_write_access_to_workspace(
                    workspace, user, request.user
                )
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
        return HttpResponseBadRequest("Something wrong happened.")

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@login_required
def switch_right(request):
    """Switch user's right for the workspace.

    Args:
        request

    Returns
    """

    workspace_id = request.POST.get("workspace_id", None)
    object_id = request.POST.get("object_id", None)
    group_or_user = request.POST.get("group_or_user", None)
    action = request.POST.get("action", None)
    value = request.POST.get("value", None) == "true"

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))

        if group_or_user == USER:
            _switch_user_right(object_id, action, value, workspace, request.user)
        if group_or_user == GROUP:
            _switch_group_right(object_id, action, value, workspace, request.user)

    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
        return HttpResponseBadRequest("Something wrong happened.")

    return HttpResponse(json.dumps({}), content_type="application/javascript")


def _switch_user_right(user_id, action, value, workspace, request_user):
    """Change the user rights to the workspace.

    Args:
        user_id:
        action:
        value:
        workspace:
        request_user:

    Returns:
    """
    user = user_api.get_user_by_id(user_id)

    if action == ACTION_READ:
        if value:
            workspace_api.add_user_read_access_to_workspace(
                workspace, user, request_user
            )
        else:
            workspace_api.remove_user_read_access_to_workspace(
                workspace, user, request_user
            )
    elif action == ACTION_WRITE:
        if value:
            workspace_api.add_user_write_access_to_workspace(
                workspace, user, request_user
            )
        else:
            workspace_api.remove_user_write_access_to_workspace(
                workspace, user, request_user
            )


def _switch_group_right(group_id, action, value, workspace, request_user):
    """Change the group rights to the workspace.

    Args:
        group_id:
        action:
        value:
        workspace:
        request_user:

    Returns:
    """
    group = group_api.get_group_by_id(group_id)

    if action == ACTION_READ:
        if value:
            workspace_api.add_group_read_access_to_workspace(
                workspace, group, request_user
            )
        else:
            workspace_api.remove_group_read_access_to_workspace(
                workspace, group, request_user
            )
    elif action == ACTION_WRITE:
        if value:
            workspace_api.add_group_write_access_to_workspace(
                workspace, group, request_user
            )
        else:
            workspace_api.remove_group_write_access_to_workspace(
                workspace, group, request_user
            )


@login_required
def remove_user_or_group_rights(request):
    """Remove user's right for the workspace.

    Args:
        request

    Returns
    """

    workspace_id = request.POST.get("workspace_id", None)
    object_id = request.POST.get("object_id", None)
    group_or_user = request.POST.get("group_or_user", None)

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))

        if group_or_user == USER:
            _remove_user_rights(object_id, workspace, request.user)
        if group_or_user == GROUP:
            _remove_group_rights(object_id, workspace, request.user)

    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except ModelError:
        return HttpResponseBadRequest("Invalid input.")
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
        return HttpResponseBadRequest("Something wrong happened.")

    return HttpResponse(json.dumps({}), content_type="application/javascript")


def _remove_user_rights(object_id, workspace, request_user):
    """Remove all user rights on the workspace.

    Args:
        object_id:
        workspace:
        request_user:

    Returns:
    """
    user = user_api.get_user_by_id(object_id)
    workspace_api.remove_user_read_access_to_workspace(workspace, user, request_user)
    workspace_api.remove_user_write_access_to_workspace(workspace, user, request_user)


def _remove_group_rights(object_id, workspace, request_user):
    """Remove all group rights on the workspace.

    Args:
        object_id:
        workspace:
        request_user:

    Returns:
    """
    group = group_api.get_group_by_id(object_id)
    workspace_api.remove_group_read_access_to_workspace(workspace, group, request_user)
    workspace_api.remove_group_write_access_to_workspace(workspace, group, request_user)


@login_required
def load_add_group_form(request):
    """Load the form to list the groups with no access to the workspace.

    Args:
        request:

    Returns:
    """
    workspace_id = request.POST.get("workspace_id", None)
    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
    except exceptions.ModelError:
        return HttpResponseBadRequest("Invalid input.")
    except Exception:
        return HttpResponseBadRequest("An unexpected error occurred.")

    try:
        # We retrieve all groups with no access
        groups_with_no_access = list(
            workspace_api.get_list_group_with_no_access_workspace(
                workspace, request.user
            )
        )

        if len(groups_with_no_access) > 0:
            group_utils.remove_list_object_from_list(
                groups_with_no_access,
                [group_api.get_anonymous_group(), group_api.get_default_group()],
            )
        if len(groups_with_no_access) == 0:
            return HttpResponseBadRequest("There is no groups that can be added.")

        form = GroupRightForm(groups_with_no_access)
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except:
        return HttpResponseBadRequest("Something wrong happened.")

    context = {"add_group_form": form}

    return HttpResponse(
        json.dumps(
            {
                "form": loader.render_to_string(
                    "core_main_app/user/workspaces/list/modals/add_group_form.html",
                    context,
                )
            }
        ),
        "application/javascript",
    )


@login_required
def add_group_right_to_workspace(request):
    """Add rights to group for the workspace.

    Args:
        request

    Returns
    """
    workspace_id = request.POST.get("workspace_id", None)
    groups_ids = request.POST.getlist("groups_id[]", [])
    is_read_checked = request.POST.get("read", None) == "true"
    is_write_checked = request.POST.get("write", None) == "true"

    if len(groups_ids) == 0:
        return HttpResponseBadRequest("You need to select at least one group.")
    if not is_read_checked and not is_write_checked:
        return HttpResponseBadRequest(
            "You need to select at least one permission (read and/or write)."
        )

    try:
        workspace = workspace_api.get_by_id(str(workspace_id))
        for group in group_api.get_all_groups_by_list_id(groups_ids):
            if is_read_checked:
                workspace_api.add_group_read_access_to_workspace(
                    workspace, group, request.user
                )
            if is_write_checked:
                workspace_api.add_group_write_access_to_workspace(
                    workspace, group, request.user
                )
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
        return HttpResponseBadRequest("Something wrong happened.")

    return HttpResponse(json.dumps({}), content_type="application/javascript")


@method_decorator(login_required, name="dispatch")
class AssignView(View):
    """Assign Ajax view"""

    api = None

    def post(self, request):
        """Assign the record to a workspace.

        Args:
            request:

        Returns:
        """
        document_ids = request.POST.getlist("document_id[]", [])
        workspace_id = request.POST.get("workspace_id", None)

        if workspace_id is None or workspace_id == "":
            workspace = None
        else:
            try:
                workspace = workspace_api.get_by_id(str(workspace_id))
            except DoesNotExist:
                return HttpResponseBadRequest(
                    "The selected workspace does not exist anymore."
                )
            except Exception:
                return HttpResponseBadRequest("Something wrong happened.")

        for data_id in document_ids:
            try:
                self.api.assign(
                    self.api.get_by_id(data_id, request.user), workspace, request.user
                )
            except AccessControlError as ace:
                return HttpResponseForbidden(escape(str(ace)))
            except Exception:
                return HttpResponseBadRequest("Something wrong happened.")

        return HttpResponse(json.dumps({}), content_type="application/javascript")


def change_data_display(request):
    """Change data display

    Args:
        request:

    Returns:
    """
    try:
        xsl_transformation_id = request.POST.get("xslt_id", None)
        data_id = request.POST.get("data_id", None)
        data = data_api.get_by_id(data_id, request.user)

        return HttpResponse(
            json.dumps(
                {
                    "template": render_xml_as_html(
                        xml_content=data.xml_content,
                        template_id=data.template.id,
                        template_hash=data.template.hash,
                        xslt_id=xsl_transformation_id,
                        request=request,
                    ),
                }
            ),
            "application/javascript",
        )
    except AccessControlError:
        return HttpResponseForbidden("Access Forbidden")
    except:
        return HttpResponseBadRequest("Unexpected error")
