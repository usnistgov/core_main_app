""" Common views
"""
import json
import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime

from django.conf import settings as conf_settings
from core_main_app import settings as main_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponse,
)
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape as html_escape, escape
from django.views.generic import View

from core_main_app.access_control import api as acl_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.commons.constants import DATA_FORMAT_FOR_TEMPLATE_FORMAT
from core_main_app.commons.exceptions import (
    DoesNotExist,
    JSONError,
)
from core_main_app.components.blob import api as blob_api
from core_main_app.components.data import api as data_api
from core_main_app.components.group import api as group_api
from core_main_app.components.lock import api as lock_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template.access_control import check_can_write
from core_main_app.components.template.models import Template
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.xsl_transformation import (
    api as xslt_transformation_api,
)
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils import file as main_file_utils
from core_main_app.utils import group as group_utils
from core_main_app.utils import xml as main_xml_utils
from core_main_app.utils.json_utils import (
    validate_json_data,
    is_schema_valid,
    load_json_string,
)
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.rendering import admin_render, render
from core_main_app.utils.view_builders import data as data_view_builder
from core_main_app.views.admin.forms import TemplateXsltRenderingForm
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


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
        except Exception:
            return HttpResponseBadRequest("Something wrong happened.")

        if workspace.owner != str(request.user.id) and not self.administration:
            return HttpResponseForbidden(
                "Only the workspace owner can edit the rights."
            )

        try:
            # Users
            users_read_workspace = (
                workspace_api.get_list_user_can_read_workspace(
                    workspace, request.user
                )
            )
            users_write_workspace = (
                workspace_api.get_list_user_can_write_workspace(
                    workspace, request.user
                )
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
        except Exception:
            detailed_users = []

        try:
            # Groups
            groups_read_workspace = (
                workspace_api.get_list_group_can_read_workspace(
                    workspace, request.user
                )
            )
            groups_write_workspace = (
                workspace_api.get_list_group_can_write_workspace(
                    workspace, request.user
                )
            )

            groups_access_workspace = list(
                set(groups_read_workspace + groups_write_workspace)
            )
            group_utils.remove_list_object_from_list(
                groups_access_workspace,
                [
                    group_api.get_anonymous_group(),
                    group_api.get_default_group(),
                ],
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
        except Exception:
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
                "core_main_app/common/css/switch.css",
                "core_main_app/common/css/select.css",
            ],
            "js": [
                {
                    "path": "core_main_app/common/js/backtoprevious.js",
                    "is_raw": True,
                },
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
                {
                    "path": "core_main_app/user/js/workspaces/init.js",
                    "is_raw": False,
                },
            ],
        }

        modals = [
            "core_main_app/user/workspaces/list/modals/add_user.html",
            "core_main_app/user/workspaces/list/modals/switch_right.html",
            "core_main_app/user/workspaces/list/modals/remove_rights.html",
            "core_main_app/user/workspaces/list/modals/add_group.html",
        ]

        # Set page title
        context.update({"page_title": "Edit Workspace"})

        return self.common_render(
            request,
            self.template,
            context=context,
            assets=assets,
            modals=modals,
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
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    }
                ],
            },
            context={
                "error": "Unable to access the requested "
                + get_data_label()
                + f": {error_message}.",
                "status_code": status_code,
                "page_title": "Error",
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
            template_xsl_rendering = (
                template_xsl_rendering_api.get_by_template_id(template_id)
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
                    xslt.id
                    for xslt in template_xsl_rendering.list_detail_xslt.all()
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
                },
                {
                    "path": "core_main_app/common/js/tooltip.js",
                    "is_raw": False,
                },
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
            request,
            self.template_name,
            context=self.context,
            assets=self.assets,
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
            return self.rendering(
                request, self.template_name, context=self.context
            )

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
            return self.rendering(
                request, self.template_name, context=self.context
            )


def defender_error_page(request):
    """Error page for defender package.

    Args:
        request:

    Returns:

    """
    return render(
        request,
        "core_main_app/common/defender/error.html",
        context={"page_title": "Error"},
    )


class AbstractEditorView(View, metaclass=ABCMeta):
    """Abstract Text Editor View"""

    template = "core_main_app/user/text_editor/text_editor.html"

    @abstractmethod
    def _get_object(self, request):
        """Returns object

        Args:

        Returns: object

        """
        raise NotImplementedError("get object is not implemented.")

    @abstractmethod
    def _check_permission(self, document, request):
        """Returns object

        Args:

        Returns: object

        """
        raise NotImplementedError("check permission is not implemented.")

    @abstractmethod
    def _prepare_context(self, document):
        """Returns object

        Args:

        Returns: object

        """
        raise NotImplementedError("prepare context is not implemented.")

    def _check_size(self, document):
        """Check content size

        Args:

        Returns:

        """
        raise NotImplementedError("prepare context is not implemented.")

    def _get_assets(self):
        """get assets

        Return:
        """
        assets = {
            "js": [
                {
                    "path": "core_main_app/user/js/text_editor/text_editor.js",
                    "is_raw": True,
                },
            ],
            "css": [
                "core_main_app/user/css/text-editor.css",
            ],
        }
        if main_settings.TEXT_EDITOR_LIBRARY == "Monaco":
            assets["js"].extend(
                [
                    {
                        "path": "core_main_app/user/js/text_editor/monaco-editor-loader.js",
                        "is_raw": True,
                    },
                    {
                        "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/loader.min.js",
                        "integrity": "sha512-ZG31AN9z/CQD1YDDAK4RUAvogwbJHv6bHrumrnMLzdCrVu4HeAqrUX7Jsal/cbUwXGfaMUNmQU04tQ8XXl5Znw==",
                        "is_external": True,
                        "is_raw": False,
                    },
                    {
                        "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.min.js",
                        "integrity": "sha512-AnszY619AdeYxGzR/u1bSnYCRmnGHrHLpOkc0qolt12NuhUJI4Cw+dRK0eiRChNxvY+C84xDE0HPPGdr3bCTZQ==",
                        "is_external": True,
                        "is_raw": False,
                    },
                    {
                        "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.nls.min.js",
                        "integrity": "sha512-E3GzU1Yj2NxL325SuAMqGvDn0W9+xr3WSkwEacvKo5Qh3wv60JToJUcIAUYrgtiF5tlwU2pztakxsp2UnHhbKA==",
                        "is_external": True,
                        "is_raw": False,
                    },
                ]
            )
            assets["external_css"] = [
                {
                    "path": "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.46.0/min/vs/editor/editor.main.min.css",
                    "integrity": "sha512-Q/ZIaWsdJBTBAkGTDqXN6AhYSD7+QEa+ccWJLsFTbayZWiv+Vi/BUGfm8E/4k/AV9Wvpci22/QSl56214Mv5NQ==",
                    "extra_args": {"data-name": "vs/editor/editor.main"},
                }
            ]

        return assets

    def _get_modals(self):
        """get assets

        Return:
        """

        return []

    def _get_context(self, document_id, document_title, type_content, content):
        """get context

        Return:
        """
        context = {
            "page_title": type_content + " Text Editor",
            "name": document_title,
            "content": content,
            "type": type_content,
            "document_id": document_id,
            "TEXT_EDITOR_LIBRARY": main_settings.TEXT_EDITOR_LIBRARY,
        }
        return context

    def post(self, request):
        """post

        Parameters:
            {
                "content":"content",
                "action": format/validate/save
                "document_id": document_id
                "template_id": template_id
            }

        Args:
            request: HTTP request

        Returns:

            - code: 200
              content: action done
            - code: 400
              content: Bad request
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """

        try:
            # get action
            action = request.POST["action"]
            # apply action: format, validate or save
            return getattr(self, "%s" % action)(request=request)
        except Exception as e:
            return HttpResponseBadRequest(html_escape(str(e)))

    def get(self, request):
        """get

        Args:
            request:

        Returns:
        """

        try:
            request = self.request
            if "id" not in request.GET:
                raise KeyError("document id is missing")
            document = self._get_object(request)
            self._check_permission(document, request)
            self._check_size(document)
            context = self._prepare_context(document)
            assets = self._get_assets()
            modals = self._get_modals()

            return render(
                request,
                self.template,
                assets=assets,
                context=context,
                modals=modals,
            )

        except AccessControlError as acl_exception:
            error_message = str(acl_exception)
            status_code = 403
        except exceptions.DoesNotExist:
            error_message = self.object_name + " not found"
            status_code = 404
        except Exception as e:
            error_message = str(e)
            status_code = 400
        return render(
            request,
            "core_main_app/common/commons/error.html",
            assets={
                "js": [
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    }
                ]
            },
            context={
                "error": error_message,
                "status_code": status_code,
            },
        )

    @abstractmethod
    def format(self, *args, **kwargs):
        """Returns formatted content

        Args:
            args:
            kwargs:

        Returns: content

        """
        raise NotImplementedError("format method is not implemented.")

    @abstractmethod
    def validate(self, *args, **kwargs):
        """Validate content

        Args:
            args:
            kwargs:

        Returns:

        """
        raise NotImplementedError("validate method is not implemented.")

    @abstractmethod
    def save(self, *args, **kwargs):
        """Save content

        Args:
            args:
            kwargs:

        Returns:

        """
        raise NotImplementedError("save method is not implemented.")

    @abstractmethod
    def generate(self, *args, **kwargs):
        """generate content

        Args:
            args:
            kwargs:

        Returns:

        """
        raise NotImplementedError("generate method is not implemented.")


class XmlEditor(AbstractEditorView, metaclass=ABCMeta):
    """Xml Editor"""

    def format(self, *args, **kwargs):
        """Format xml content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        return HttpResponse(
            json.dumps(main_xml_utils.format_content_xml(content)),
            "application/javascript",
        )

    def validate(self, *args, **kwargs):
        """Validate xml content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()

        try:
            # build the xsd tree
            xml_tree = XSDTree.build_tree(content)
        except Exception as exception:
            raise exceptions.XMLError(str(exception))
        try:
            # get template
            template_id = self.request.POST["template_id"]
            template = template_api.get_by_id(template_id, self.request)
            # build the xsd tree
            xsd_tree = XSDTree.build_tree(template.content)
        except Exception as exception:
            raise exceptions.XSDError(str(exception))

        # validate content
        error = main_xml_utils.validate_xml_data(
            xsd_tree, xml_tree, request=self.request
        )
        if error is not None:
            raise exceptions.XMLError(error)
        return HttpResponse(
            json.dumps("Validated successfully"),
            "application/javascript",
        )

    def generate(self, *args, **kwargs):
        """Generate xml content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        template_id = self.request.POST["template_id"]

        if "core_curate_app" not in conf_settings.INSTALLED_APPS:
            raise exceptions.CoreError(
                "The Curate App needs to be installed to use this feature."
            )

        if content:
            raise exceptions.XMLError(
                "Please clear form before generating a new XML document."
            )

        from core_main_app.utils.parser import get_parser
        from core_parser_app.components.data_structure_element import (
            api as data_structure_element_api,
        )
        from core_curate_app.components.curate_data_structure.models import (
            CurateDataStructure,
        )
        from core_curate_app.components.curate_data_structure import (
            api as curate_data_structure_api,
        )
        from core_curate_app.views.user import views as curate_views

        # Get template
        template = template_api.get_by_id(template_id, self.request)
        # Create temp data structure
        curate_data_structure = CurateDataStructure(
            user=str(self.request.user.id),
            template=template,
            name="text_editor_tmp_" + str(datetime.now()),
        )
        # create new curate data structure
        curate_data_structure_api.upsert(
            curate_data_structure, self.request.user
        )
        # build parser
        parser = get_parser(request=self.request)
        # generate form
        root_element_id = parser.generate_form(
            xsd_doc_data=template.content,
            xml_doc_data=None,
            data_structure=curate_data_structure,
            request=self.request,
        )
        # get the root element
        root_element = data_structure_element_api.get_by_id(
            root_element_id, self.request
        )

        # generate xml string
        xml_data = curate_views.render_xml(self.request, root_element)

        # prettify content
        xml_data = main_xml_utils.format_content_xml(xml_data)

        # delete temp data structure
        curate_data_structure_api.delete(
            curate_data_structure, self.request.user
        )

        return HttpResponse(
            json.dumps(xml_data),
            "application/javascript",
        )

    def _get_assets(self):
        """get assets

        Return:
        """
        # get assets
        assets = super()._get_assets()

        # add css relatives to xml editor
        assets["css"].append("core_main_app/common/css/XMLTree.css")

        # add js relatives to xml editor
        assets["js"].append(
            {
                "path": "core_main_app/common/js/XMLTree.js",
                "is_raw": False,
            }
        )
        assets["js"].append(
            {
                "path": "core_main_app/user/js/text_editor/data_text_editor.raw.js",
                "is_raw": True,
            }
        )
        return assets

    def get_context(self, document, document_title, xml_content):
        """get context

        Args:
            document:
            document_title:
            xml_content:

        Returns:
        """
        # try to format before build context
        try:
            xml_content = main_xml_utils.format_content_xml(xml_content)
        except exceptions.XMLError as exception:
            logger.warning(str(exception))

        # get context
        context = super()._get_context(
            document.id,
            document_title,
            DATA_FORMAT_FOR_TEMPLATE_FORMAT[document.template.format],
            xml_content,
        )

        # build xslt selector
        (
            display_xslt_selector,
            template_xsl_rendering,
            xsl_transformation_id,
        ) = data_view_builder.xslt_selector(document.template.id)

        # add context relatives to xml editor
        context.update(
            {
                "document_name": document.__class__.__name__,
                "template_id": document.template.id,
                "template_xsl_rendering": template_xsl_rendering,
                "xsl_transformation_id": xsl_transformation_id,
                "can_display_selector": display_xslt_selector,
            }
        )

        return context


class JSONEditor(AbstractEditorView, metaclass=ABCMeta):
    """JSON Editor"""

    def format(self, *args, **kwargs):
        """Format json content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        json_object = load_json_string(content)

        return HttpResponse(
            json.dumps(json_object, indent=2),
            "application/javascript",
        )

    def validate(self, *args, **kwargs):
        """Validate json content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        try:
            # get template
            template_id = self.request.POST["template_id"]
            template = template_api.get_by_id(template_id, self.request)
        except Exception as exception:
            return HttpResponseBadRequest(escape(str(exception)))

        try:  # validate content
            validate_json_data(content, template.content)
        except JSONError as json_error:
            return HttpResponseBadRequest(
                json.dumps(
                    [
                        html_escape(str(message))
                        for message in json_error.message_list
                    ]
                )
            )
        except Exception as exc:
            raise JSONError(str(exc))

        return HttpResponse(
            json.dumps("Validated successfully"),
            "application/javascript",
        )

    def _get_assets(self):
        """get assets

        Return:
        """
        # get assets
        assets = super()._get_assets()

        assets["js"].append(
            {
                "path": "core_main_app/user/js/text_editor/data_text_editor.raw.js",
                "is_raw": True,
            }
        )
        return assets

    def get_context(self, document, document_title, json_content):
        """get context

        Args:
            document:
            document_title:
            json_content:

        Returns:
        """
        # format before build context
        json_content.strip()

        # get assets
        context = super()._get_context(
            document.id,
            document_title,
            DATA_FORMAT_FOR_TEMPLATE_FORMAT[document.template.format],
            json_content,
        )

        # add context relatives to json editor
        context.update(
            {
                "document_name": document.__class__.__name__,
                "template_id": document.template.id,
            }
        )

        return context

    def generate(self, *args, **kwargs):
        """generate content

        Args:
            args:
            kwargs:

        Returns:

        """
        raise NotImplementedError("generate method is not implemented.")


class DataMixin:
    object_name = get_data_label()

    def _get_object(self, request):
        """get data

        Args:
            request:

        Returns:

        """
        return data_api.get_by_id(request.GET["id"], request.user)

    def _check_permission(self, data, request):
        """check user permission

        Args:
            data:
            request:

        Returns:

        """
        acl_api.check_can_write(data, request.user)

    def _check_size(self, data):
        """check content size

        Args:
            data:

        Returns:

        """

        if (
            main_file_utils.get_byte_size_from_string(data.content)
            > MAX_DOCUMENT_EDITING_SIZE
        ):
            raise exceptions.DocumentEditingSizeError(
                "The file is too large (MAX_DOCUMENT_EDITING_SIZE)."
            )

    def save(self, *args, **kwargs):
        """Save data content

        Args:
            *args:
            **kwargs:

        Returns:

        """
        try:
            request = kwargs.get("request")
            content = request.POST["content"].strip()
            data_id = request.POST["document_id"]
            data = data_api.get_by_id(data_id, request.user)
            # update content
            data.content = content
            # save data
            data_api.upsert(data, request)
            lock_api.remove_lock_on_object(data, request.user)
            messages.add_message(
                request,
                messages.SUCCESS,
                get_data_label().capitalize() + " saved with success.",
            )
            return HttpResponse(
                json.dumps({"url": reverse("core_main_app_homepage")}),
                "application/javascript",
            )
        except AccessControlError as ace:
            return HttpResponseForbidden(html_escape(str(ace)))
        except DoesNotExist as dne:
            return HttpResponseBadRequest(html_escape(str(dne)))
        except Exception as e:
            return HttpResponseBadRequest(html_escape(str(e)))


class TemplateMixin:
    object_name = "Template"

    def _get_object(self, request):
        """get object

        Args:
            request:

        Returns:

        """
        return template_api.get_by_id(request.GET["id"], request)

    def _prepare_context(self, template):
        """prepare context

        Args:
            template:

        Returns:

        """
        return self._get_context(
            template.id, template.filename, template.format, template.content
        )

    def _check_permission(self, template, request):
        """check user permission

        Args:
            template:
            request:

        Returns:

        """
        check_can_write(template, request=request)

    def _check_size(self, template):
        """check content size

        Args:
            template:

        Returns:

        """

        if (
            main_file_utils.get_byte_size_from_string(template.content)
            > MAX_DOCUMENT_EDITING_SIZE
        ):
            raise exceptions.DocumentEditingSizeError(
                "The file is too large (MAX_DOCUMENT_EDITING_SIZE)."
            )

    def save(self, *args, **kwargs):
        """Save template content

        Args:
            *args:
            **kwargs:

        Returns:

        """
        try:
            request = kwargs.get("request")
            content = request.POST["content"].strip()
            template_id = request.POST["document_id"]
            template = template_api.get_by_id(template_id, request)
            if template.format == Template.JSON:
                content = load_json_string(content)
            # update content
            template.content = content
            # save template
            template_api.upsert(template, request=request)
            return HttpResponse(
                json.dumps({"url": reverse("core_main_app_homepage")}),
                "application/javascript",
            )
        except AccessControlError as ace:
            return HttpResponseForbidden(html_escape(str(ace)))
        except DoesNotExist as dne:
            return HttpResponseBadRequest(html_escape(str(dne)))
        except Exception as e:
            return HttpResponseBadRequest(html_escape(str(e)))


class DataXMLEditor(DataMixin, XmlEditor):
    """Data XML Editor View"""

    def _prepare_context(self, data):
        """prepare context

        Args:
            data:

        Returns:

        """
        lock_api.set_lock_object(data, self.request.user)
        return self.get_context(data, data.title, data.content)


class TemplateXSDEditor(TemplateMixin, XmlEditor):
    """Template XSD Editor View"""

    def validate(self, *args, **kwargs):
        """Validate xml content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        try:
            # build the xsd tree
            xsd_tree = XSDTree.build_tree(content)
        except Exception as exception:
            raise exceptions.XSDError(str(exception))

        # validate the schema
        error = main_xml_utils.validate_xml_schema(
            xsd_tree, request=self.request
        )
        if error is not None:
            raise exceptions.XMLError(error)

        return HttpResponse(
            json.dumps("Validated successfully"),
            "application/javascript",
        )


class DataJSONEditor(DataMixin, JSONEditor):
    """JSON Editor View"""

    def _prepare_context(self, data):
        """prepare context

        Args:
            data:

        Returns:

        """
        lock_api.set_lock_object(data, self.request.user)
        return self.get_context(data, data.title, data.content)


class TemplateJSONEditor(TemplateMixin, JSONEditor):
    """Template JSON Editor View"""

    def validate(self, *args, **kwargs):
        """Validate JSON content

        Args:
            args:
            kwargs:

        Returns:

        """
        content = self.request.POST["content"].strip()
        try:
            # validate content
            is_schema_valid(content)
        except Exception as e:
            raise JSONError(str(e))

        return HttpResponse(
            json.dumps("Validated successfully"),
            "application/javascript",
        )


class ViewBlob(CommonView):
    """
    View blob.
    """

    template = "core_main_app/user/blob/detail.html"

    def get(self, request, *args, **kwargs):
        """get

        Args:
            request:

        Returns:
        """
        blob_id = request.GET["id"]

        try:
            # Get blob
            blob_object = blob_api.get_by_id(blob_id, request.user)
            try:
                acl_api.check_can_write(blob_object, request.user)
                can_write = True
            except AccessControlError:
                can_write = False
            # Init context
            context = {"blob": blob_object, "can_write": can_write}
            # Init assets
            assets = {
                "js": [
                    {
                        "path": "core_main_app/user/js/blob/detail.js",
                        "is_raw": False,
                    }
                ],
                "css": [],
            }

            context.update({"page_title": "View File"})

            return self.common_render(
                request,
                self.template,
                assets=assets,
                context=context,
            )
        except exceptions.DoesNotExist:
            error_message = "Blob not found"
            status_code = 404
        except AccessControlError:
            error_message = "Access Forbidden"
            status_code = 403
        except Exception as e:
            error_message = str(e)
            status_code = 400

        return self.common_render(
            request,
            "core_main_app/common/commons/error.html",
            context={
                "error": "Unable to access the requested file"
                + f": {error_message}.",
                "status_code": status_code,
                "page_title": "Error",
            },
        )


class ManageBlobMetadata(CommonView):
    """
    Manage blob metadata.
    """

    template = "core_main_app/user/blob/detail_metadata.html"

    def get(self, request, pk, *args, **kwargs):
        """get

        Args:
            request:
            pk:

        Returns:
        """

        try:
            # Get blob
            blob_object = blob_api.get_by_id(pk, request.user)
            try:
                acl_api.check_can_write(blob_object, request.user)
                can_write = True
            except AccessControlError:
                can_write = False
            # Init context
            context = {"blob": blob_object, "can_write": can_write}
            # Init modals
            modals = [
                "core_main_app/user/blob/list/modals/add_metadata.html",
            ]
            # Init assets
            assets = {
                "js": [
                    {
                        "path": "core_main_app/user/js/blob/detail.js",
                        "is_raw": False,
                    },
                    {
                        "path": "core_main_app/user/js/blob/blob_metadata.js",
                        "is_raw": False,
                    },
                ],
                "css": [
                    "core_main_app/common/css/select.css",
                ],
            }

            context.update({"page_title": "File Metadata"})

            return self.common_render(
                request,
                self.template,
                modals=modals,
                assets=assets,
                context=context,
            )
        except exceptions.DoesNotExist:
            error_message = "Blob not found"
            status_code = 404
        except AccessControlError:
            error_message = "Access Forbidden"
            status_code = 403
        except Exception as e:
            error_message = str(e)
            status_code = 400

        return self.common_render(
            request,
            "core_main_app/common/commons/error.html",
            context={
                "error": "Unable to access the requested file "
                + f": {error_message}.",
                "status_code": status_code,
                "page_title": "Error",
            },
        )
