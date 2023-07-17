""" Ajax API
"""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.template import loader
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import View

from core_main_app.access_control.api import check_can_write
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_main_app.components.blob import api as blob_api
from core_main_app.components.blob.models import Blob
from core_main_app.components.data import api as data_api
from core_main_app.components.group import api as group_api
from core_main_app.components.template import api as template_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.templatetags.xsl_transform_tag import (
    render_xml_as_html_detail,
)
from core_main_app.utils import group as group_utils
from core_main_app.views.user.forms import (
    ChangeWorkspaceForm,
    UserRightForm,
    GroupRightForm,
    BlobMetadataForm,
    BlobFileForm,
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
                request.user,
                list(),
                is_administration,
                self.show_global_workspace,
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
            users_with_no_access.remove(
                user_api.get_user_by_id(workspace.owner)
            )

        if len(users_with_no_access) == 0:
            return HttpResponseBadRequest(
                "There are no users that can be added."
            )

        form = UserRightForm(users_with_no_access)
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
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
            _switch_user_right(
                object_id, action, value, workspace, request.user
            )
        if group_or_user == GROUP:
            _switch_group_right(
                object_id, action, value, workspace, request.user
            )

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
    workspace_api.remove_user_read_access_to_workspace(
        workspace, user, request_user
    )
    workspace_api.remove_user_write_access_to_workspace(
        workspace, user, request_user
    )


def _remove_group_rights(object_id, workspace, request_user):
    """Remove all group rights on the workspace.

    Args:
        object_id:
        workspace:
        request_user:

    Returns:
    """
    group = group_api.get_group_by_id(object_id)
    workspace_api.remove_group_read_access_to_workspace(
        workspace, group, request_user
    )
    workspace_api.remove_group_write_access_to_workspace(
        workspace, group, request_user
    )


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
                [
                    group_api.get_anonymous_group(),
                    group_api.get_default_group(),
                ],
            )
        if len(groups_with_no_access) == 0:
            return HttpResponseBadRequest(
                "There are no groups that can be added."
            )

        form = GroupRightForm(groups_with_no_access)
    except AccessControlError as ace:
        return HttpResponseBadRequest(escape(str(ace)))
    except DoesNotExist as dne:
        return HttpResponseBadRequest(escape(str(dne)))
    except Exception:
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
                    self.api.get_by_id(data_id, request.user),
                    workspace,
                    request.user,
                )
            except AccessControlError as ace:
                return HttpResponseForbidden(escape(str(ace)))
            except Exception:
                return HttpResponseBadRequest("Something wrong happened.")

        return HttpResponse(
            json.dumps({}), content_type="application/javascript"
        )


def change_data_display(request):
    """Change data display

    Args:
        request:

    Returns:
    """
    try:
        xsl_transformation_id = request.POST.get("xslt_id", None)
        data_id = request.POST.get("data_id", None)
        if data_id:
            data = data_api.get_by_id(data_id, request.user)
            template_id = data.template.id
            template_hash = data.template.hash
            xml_content = data.xml_content
        else:
            template_id = request.POST.get("template_id", None)
            xml_content = request.POST.get("content", "")
            if template_id:
                template = template_api.get_by_id(template_id, request)
                template_hash = template.hash
            else:
                return HttpResponseBadRequest(
                    "missing parameters: template id is missing"
                )
        return HttpResponse(
            json.dumps(
                {
                    "template": render_xml_as_html_detail(
                        xml_content=xml_content,
                        template_id=template_id,
                        template_hash=template_hash,
                        xslt_id=xsl_transformation_id,
                        request=request,
                    ),
                }
            ),
            "application/javascript",
        )
    except AccessControlError:
        return HttpResponseForbidden("Access Forbidden")
    except Exception:
        return HttpResponseBadRequest("Unexpected error")


@method_decorator(login_required, name="dispatch")
class LoadBlobMetadataForm(View):
    """Load the form to add metadata files to a blob."""

    def get(self, request):
        """Load the form to add metadata files to a blob.

        Args:
            request:

        Returns:

        """
        blob_id = request.GET.get("blob_id", None)

        try:
            blob_object = blob_api.get_by_id(str(blob_id), request.user)
            form = BlobMetadataForm(user=request.user, blob=blob_object)
        except exceptions.ModelError:
            return HttpResponseBadRequest("Blob not found.")
        except Exception:
            return HttpResponseBadRequest("An unexpected error occurred.")

        context = {"add_metadata_form": form}

        return HttpResponse(
            json.dumps(
                {
                    "form": loader.render_to_string(
                        "core_main_app/user/blob/list/modals/add_metadata_form.html",
                        context,
                    )
                }
            ),
            "application/javascript",
        )


@method_decorator(login_required, name="dispatch")
class AddMetadataToBlob(View):
    """Add metadata files to a blob."""

    def post(self, request):
        """Add metadata files to a blob.

        Args:
            request:

        Returns:

        """
        blob_id = request.POST.get("blob_id", None)
        metadata_id_list = request.POST.getlist("metadata_id[]", [])

        try:
            blob_object = blob_api.get_by_id(str(blob_id), request.user)
            check_can_write(blob_object, request.user)
            blob_api.add_metadata_list(
                blob_object,
                [
                    data_api.get_by_id(metadata_id, request.user)
                    for metadata_id in metadata_id_list
                ],
                request.user,
            )
        except exceptions.ModelError:
            return HttpResponseBadRequest("Blob not found.")
        except AccessControlError:
            return HttpResponseBadRequest("Permission denied.")
        except Exception:
            return HttpResponseBadRequest("An unexpected error occurred.")

        messages.add_message(
            request,
            messages.SUCCESS,
            "Metadata updated.",
        )
        return HttpResponse(json.dumps({}), "application/javascript")


@method_decorator(login_required, name="dispatch")
class RemoveMetadataFromBlob(View):
    """Remove metadata file from blob."""

    def post(self, request):
        """Remove metadata file

        Args:
            request:

        Returns:

        """
        blob_id = request.POST.get("blob_id", None)
        metadata_id = request.POST.get("metadata_id", None)

        try:
            blob_object = blob_api.get_by_id(str(blob_id), request.user)
            check_can_write(blob_object, request.user)
            metadata = data_api.get_by_id(metadata_id, request.user)
            blob_api.remove_metadata(blob_object, metadata, request.user)
        except exceptions.ModelError:
            return HttpResponseBadRequest("Blob not found.")
        except AccessControlError:
            return HttpResponseBadRequest("Permission denied.")
        except Exception:
            return HttpResponseBadRequest("An unexpected error occurred.")

        messages.add_message(
            request,
            messages.INFO,
            "Metadata successfully removed.",
        )
        return HttpResponse(json.dumps({}), "application/javascript")


@method_decorator(login_required, name="dispatch")
class UploadFile(View):
    """Upload file"""

    def post(self, request):
        """Upload file

        Args:
            request:

        Returns:

        """
        try:
            form = BlobFileForm(request.POST, request.FILES)
            if form.is_valid():
                blob = Blob(
                    filename=form.files["file"].name,
                    blob=form.files["file"],
                    user_id=str(request.user.id),
                )
                blob_api.insert(blob, request.user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "File successfully uploaded.",
                )
                return HttpResponse(json.dumps({}))
            else:
                return HttpResponseBadRequest(
                    json.dumps({"message": str(form.errors.as_text())})
                )
        except Exception:
            messages.add_message(
                request,
                messages.ERROR,
                "An error occurred during file upload.",
            )

            return HttpResponseBadRequest(json.dumps({}))
