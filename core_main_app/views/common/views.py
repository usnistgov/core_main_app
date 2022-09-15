"""
    Common views
"""
from abc import ABCMeta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape as html_escape
from django.views.generic import View

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data import api as data_api
from core_main_app.components.group import api as group_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.xsl_transformation import api as xslt_transformation_api
from core_main_app.utils import group as group_utils
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.rendering import admin_render
from core_main_app.utils.rendering import render
from core_main_app.utils.view_builders import data as data_view_builder
from core_main_app.views.admin.forms import TemplateXsltRenderingForm


class CommonView(View, metaclass=ABCMeta):
    """
    Abstract common view for admin and user.
    """

    administration = False

    def common_render(
        self, request, template_name, modals=None, assets=None, context=None
    ):
        """common_render

        Args:
            request:
            template_name:
            modals:
            assets:
            context:

        Returns:
        """
        return (
            admin_render(request, template_name, modals, assets, context)
            if self.administration
            else render(request, template_name, modals, assets, context)
        )

    def is_administration(self):
        """is_administration

        Returns:
        """
        return self.administration


@method_decorator(login_required, name="dispatch")
class EditWorkspaceRights(CommonView):
    """
    Edit workspace rights
    """

    template = "core_main_app/user/workspaces/edit_rights.html"

    def get(self, request, *args, **kwargs):
        """get

        Args:
            request:

        Returns:
        """

        try:
            workspace_id = kwargs["workspace_id"]
            workspace = workspace_api.get_by_id(workspace_id)
        except DoesNotExist:
            return HttpResponseBadRequest("The workspace does not exist.")
        except:
            return HttpResponseBadRequest("Something wrong happened.")

        if workspace.owner != str(request.user.id) and not self.administration:
            return HttpResponseForbidden(
                "Only the workspace owner can edit the rights."
            )

        try:
            # Users
            users_read_workspace = workspace_api.get_list_user_can_read_workspace(
                workspace, request.user
            )
            users_write_workspace = workspace_api.get_list_user_can_write_workspace(
                workspace, request.user
            )

            users_access_workspace = list(
                set(users_read_workspace + users_write_workspace)
            )
            detailed_users = []
            for user in users_access_workspace:
                if str(user.id) != workspace.owner:
                    detailed_users.append(
                        {
                            "object_id": user.id,
                            "object_name": user.username,
                            "can_read": user in users_read_workspace,
                            "can_write": user in users_write_workspace,
                        }
                    )
        except:
            detailed_users = []

        try:
            # Groups
            groups_read_workspace = workspace_api.get_list_group_can_read_workspace(
                workspace, request.user
            )
            groups_write_workspace = workspace_api.get_list_group_can_write_workspace(
                workspace, request.user
            )

            groups_access_workspace = list(
                set(groups_read_workspace + groups_write_workspace)
            )
            group_utils.remove_list_object_from_list(
                groups_access_workspace,
                [group_api.get_anonymous_group(), group_api.get_default_group()],
            )
            detailed_groups = []
            for group in groups_access_workspace:
                detailed_groups.append(
                    {
                        "object_id": group.id,
                        "object_name": group.name,
                        "can_read": group in groups_read_workspace,
                        "can_write": group in groups_write_workspace,
                    }
                )
        except:
            detailed_groups = []

        context = {
            "workspace": workspace,
            "user_data": detailed_users,
            "group_data": detailed_groups,
            "template": "core_main_app/user/workspaces/list/edit_rights_table.html",
            "action_read": "action_read",
            "action_write": "action_write",
        }

        if workspace_api.is_workspace_public(workspace):
            context.update({"is_public": True})
        if workspace_api.is_workspace_global(workspace):
            context.update({"is_global": True})

        assets = {
            "css": [
                "core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css",
                "core_main_app/libs/fSelect/css/fSelect.css",
                "core_main_app/common/css/switch.css",
            ],
            "js": [
                {
                    "path": "core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js",
                    "is_raw": True,
                },
                {"path": "core_main_app/libs/fSelect/js/fSelect.js", "is_raw": False},
                {"path": "core_main_app/common/js/backtoprevious.js", "is_raw": True},
                {"path": "core_main_app/user/js/workspaces/tables.js", "is_raw": True},
                {
                    "path": "core_main_app/user/js/workspaces/add_user.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/workspaces/list/modals/switch_right.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/workspaces/list/modals/remove_rights.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/user/js/workspaces/add_group.js",
                    "is_raw": False,
                },
                {"path": "core_main_app/user/js/workspaces/init.js", "is_raw": False},
            ],
        }

        modals = [
            "core_main_app/user/workspaces/list/modals/add_user.html",
            "core_main_app/user/workspaces/list/modals/switch_right.html",
            "core_main_app/user/workspaces/list/modals/remove_rights.html",
            "core_main_app/user/workspaces/list/modals/add_group.html",
        ]

        return self.common_render(
            request, self.template, context=context, assets=assets, modals=modals
        )


class ViewData(CommonView):
    """
    View detail data.
    """

    template = "core_main_app/user/data/detail.html"

    def get(self, request, *args, **kwargs):
        """get

        Args:
            request:

        Returns:
        """
        data_id = request.GET["id"]

        try:
            data_object = data_api.get_by_id(data_id, request.user)
            page_context = data_view_builder.build_page(
                data_object, display_download_options=True
            )

            return data_view_builder.render_page(
                request, self.common_render, self.template, page_context
            )
        except exceptions.DoesNotExist:
            error_message = "Data not found"
            status_code = 404
        except exceptions.ModelError:
            error_message = "Model error"
            status_code = 400
        except AccessControlError:
            error_message = "Access Forbidden"
            status_code = 403
        except Exception as e:
            error_message = str(e)
            status_code = 400

        return self.common_render(
            request,
            "core_main_app/common/commons/error.html",
            assets={
                "js": [
                    {"path": "core_main_app/user/js/data/detail.js", "is_raw": False}
                ]
            },
            context={
                "error": "Unable to access the requested "
                + get_data_label()
                + f": {error_message}.",
                "status_code": status_code,
            },
        )


def read_xsd_file(xsd_file):
    """Return the content of the file uploaded using Django FileField.

    Returns:

    """
    # put the cursor at the beginning of the file
    xsd_file.seek(0)
    # read the content of the file
    return xsd_file.read().decode("utf-8")


@method_decorator(login_required, name="dispatch")
class TemplateXSLRenderingView(View):
    """Template XSL rendering view."""

    rendering = render
    save_redirect = "core_main_app_manage_template_versions"
    back_to_url = "core_main_app_manage_template_versions"
    form_class = TemplateXsltRenderingForm
    template_name = "core_main_app/common/templates_xslt/main.html"
    context = {}
    assets = {}

    def get(self, request, *args, **kwargs):
        """GET request. Create/Show the form for the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        template_id = kwargs.pop("template_id")
        # Get the template
        template = template_api.get_by_id(template_id, request=request)
        # Get template information (version)
        version_manager = template.version_manager
        version_number = version_manager_api.get_version_number(
            version_manager, template_id, request=request
        )
        try:
            # Get the existing configuration to build the form
            template_xsl_rendering = template_xsl_rendering_api.get_by_template_id(
                template_id
            )
            data = {
                "id": str(template_xsl_rendering.id),
                "template": str(template.id),
                "list_xslt": template_xsl_rendering.list_xslt.id
                if template_xsl_rendering.list_xslt
                else None,
                "default_detail_xslt": template_xsl_rendering.default_detail_xslt.id
                if template_xsl_rendering.default_detail_xslt
                else None,
                "list_detail_xslt": [
                    xslt.id for xslt in template_xsl_rendering.list_detail_xslt.all()
                ]
                if template_xsl_rendering.list_detail_xslt.count()
                else None,
            }
        except (Exception, exceptions.DoesNotExist):
            # If no configuration, new form with pre-selected fields.
            data = {
                "template": str(template.id),
                "list_xslt": None,
                "default_detail_xslt": None,
                "list_detail_xslt": None,
            }

        self.assets = {
            "css": ["core_main_app/admin/css/templates_xslt/form.css"],
            "js": [
                {
                    "path": "core_main_app/admin/js/templates_xslt/detail_xslt.js",
                    "is_raw": False,
                }
            ],
        }

        self.context = {
            "template_title": template.version_manager.title,
            "template_version": version_number,
            "form_template_xsl_rendering": self.form_class(data),
            "url_back_to": reverse(
                self.back_to_url,
                kwargs={"version_manager_id": template.version_manager.id},
            ),
        }

        return self.rendering(
            request, self.template_name, context=self.context, assets=self.assets
        )

    def post(self, request, *args, **kwargs):
        """POST request. Try to save the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        form = self.form_class(request.POST, request.FILES)
        self.context.update({"form_template_xsl_rendering": form})

        if form.is_valid():
            return self._save_template_xslt(request)
        else:
            # Display error from the form
            return self.rendering(request, self.template_name, context=self.context)

    def _save_template_xslt(self, request):
        """Save a template xslt rendering.

        Args:
            request: Request.

        """
        try:
            # Get the list xslt instance
            try:
                list_xslt = xslt_transformation_api.get_by_id(
                    request.POST.get("list_xslt")
                )
            except (Exception, exceptions.DoesNotExist):
                list_xslt = None

            # Get the list detail xslt instance
            try:
                list_detail_xslt = xslt_transformation_api.get_by_id_list(
                    request.POST.getlist("list_detail_xslt")
                )
            except (Exception, exceptions.DoesNotExist):
                list_detail_xslt = None

            # Get the default detail xslt instance
            try:
                default_detail_xslt = xslt_transformation_api.get_by_id(
                    request.POST.get("default_detail_xslt")
                )
            except (Exception, exceptions.DoesNotExist):
                default_detail_xslt = None

            # Get template by id
            template = template_api.get_by_id(
                request.POST.get("template"), request=request
            )

            template_xsl_rendering_api.add_or_delete(
                template_xsl_rendering_id=request.POST.get("id"),
                template=template,
                list_xslt=list_xslt,
                default_detail_xslt=default_detail_xslt,
                list_detail_xslt=list_detail_xslt,
            )

            return HttpResponseRedirect(
                reverse(self.save_redirect, args=[template.version_manager.id])
            )
        except Exception as e:
            self.context.update({"errors": html_escape(str(e))})
            return self.rendering(request, self.template_name, context=self.context)


def defender_error_page(request):
    """Error page for defender package.

    Args:
        request:

    Returns:

    """
    return render(request, "core_main_app/common/defender/error.html")
