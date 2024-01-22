"""
    Admin views
"""
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape as html_escape
from django.views.debug import SafeExceptionReporterFilter
from django.views.generic import View
from markdown import markdown

from core_main_app.commons import constants as constants
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.web_page.models import WebPage
from core_main_app.components.xsl_transformation import (
    api as xslt_transformation_api,
)
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.templatetags.stripjs import stripjs
from core_main_app.utils.rendering import admin_render
from core_main_app.utils.xml import get_imports_and_includes
from core_main_app.views.admin.ajax import EditXSLTView
from core_main_app.views.admin.forms import TextAreaForm
from core_main_app.views.admin.forms import (
    UploadTemplateForm,
    UploadVersionForm,
    UploadXSLTForm,
)
from core_main_app.views.common.ajax import (
    EditTemplateVersionManagerView,
    DeleteObjectModalView,
)
from core_main_app.views.common.views import read_xsd_file
from core_main_app.views.user.views import get_context_manage_template_versions
from xml_utils.commons.exceptions import HTMLError
from xml_utils.html_tree.parser import parse_html


@staff_member_required
def admin_home(request):
    """Admin home view.

    Args:
        request:

    Returns:

    """
    return admin_render(request, "core_main_app/admin/dashboard.html")


class ManageTemplatesView(View):
    """Manage Templates view."""

    template_name = "core_main_app/admin/templates/list.html"

    def get(self, request):
        """get request

        Args:
            request:

        Returns:
        """

        # get all current templates
        templates = template_version_manager_api.get_global_version_managers(
            request=request
        )

        context = {
            "object_name": "Template",
            "available": [
                template for template in templates if not template.is_disabled
            ],
            "disabled": [
                template for template in templates if template.is_disabled
            ],
        }

        assets = {
            "css": ["core_main_app/common/css/template/template_ordering.css"],
            "js": [
                {
                    "path": "core_main_app/common/js/templates/list/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/tooltip.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/sort.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/list/modals/disable.js",
                    "is_raw": False,
                },
                EditTemplateVersionManagerView.get_modal_js_path(),
            ],
        }

        modals = [
            "core_main_app/admin/templates/list/modals/disable.html",
            EditTemplateVersionManagerView.get_modal_html_path(),
        ]

        return admin_render(
            request,
            self.template_name,
            assets=assets,
            context=context,
            modals=modals,
        )


@staff_member_required
def manage_template_versions(request, version_manager_id):
    """View that allows template versions management.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    try:
        # get the version manager
        version_manager = template_version_manager_api.get_by_id(
            version_manager_id, request=request
        )
        context = get_context_manage_template_versions(version_manager)
        if "core_parser_app" in settings.INSTALLED_APPS:
            context.update(
                {"module_url": "core-admin:core_parser_app_template_modules"}
            )

        assets = {
            "js": [
                {
                    "path": "core_main_app/common/js/templates/versions/set_current.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/restore.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/templates/versions/modals/disable.js",
                    "is_raw": False,
                },
            ]
        }

        modals = ["core_main_app/admin/templates/versions/modals/disable.html"]

        return admin_render(
            request,
            "core_main_app/admin/templates/versions.html",
            assets=assets,
            modals=modals,
            context=context,
        )
    except Exception as exception:
        return admin_render(
            request,
            "core_main_app/common/commons/error.html",
            context={"error": str(exception)},
        )


@staff_member_required
def upload_template(request):
    """Upload template.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependency_resolver.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
            {
                "path": "core_main_app/common/js/backtoprevious.js",
                "is_raw": True,
            },
        ]
    }

    context = {
        "object_name": "Template",
        "url": reverse("core-admin:core_main_app_upload_template"),
        "redirect_url": reverse("core-admin:core_main_app_templates"),
    }

    # method is POST
    if request.method == "POST":
        form = UploadTemplateForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_template(request, assets, context)

        # Display error from the form
        return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context["upload_form"] = UploadTemplateForm()
        return _upload_template_response(request, assets, context)


@staff_member_required
def upload_template_version(request, version_manager_id):
    """Upload template version.

    Args:
        request:
        version_manager_id:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/upload/dependency_resolver.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/admin/js/templates/upload/dependencies.js",
                "is_raw": False,
            },
        ]
    }

    template_version_manager = template_version_manager_api.get_by_id(
        version_manager_id, request=request
    )
    context = {
        "object_name": "Template",
        "version_manager": template_version_manager,
        "url": reverse(
            "core-admin:core_main_app_upload_template_version",
            kwargs={"version_manager_id": template_version_manager.id},
        ),
        "redirect_url": reverse(
            "core-admin:core_main_app_manage_template_versions",
            kwargs={"version_manager_id": template_version_manager.id},
        ),
    }

    # method is POST
    if request.method == "POST":
        form = UploadVersionForm(request.POST, request.FILES)
        context["upload_form"] = form

        if form.is_valid():
            return _save_template_version(
                request, assets, context, template_version_manager
            )

        # Display errors from the form
        return _upload_template_response(request, assets, context)
    # method is GET
    else:
        # render the form to upload a template
        context["upload_form"] = UploadVersionForm()
        return _upload_template_response(request, assets, context)


def _save_template(request, assets, context):
    """Save a template.

    Args:
        request:
        assets:
        context:

    Returns:

    """
    try:
        # get the schema name
        name = request.POST["name"]
        # get the file from the form
        xsd_file = request.FILES["upload_file"]
        # read the content of the file
        xsd_data = read_xsd_file(xsd_file)

        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager = TemplateVersionManager(title=name)
        template_version_manager_api.insert(
            template_version_manager, template, request=request
        )
        return HttpResponseRedirect(
            reverse("core-admin:core_main_app_templates")
        )
    except exceptions.XSDError as xsd_error:
        return handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except exceptions.NotUniqueError:
        context["errors"] = html_escape(
            "A template with the same name already exists. Please choose another name."
        )
        return _upload_template_response(request, assets, context)
    except Exception as exception:
        context["errors"] = html_escape(str(exception))
        return _upload_template_response(request, assets, context)


def _save_template_version(request, assets, context, template_version_manager):
    """Save a template version.

    Args:
        request:
        assets:
        context:
        template_version_manager:

    Returns:

    """

    try:
        # get the file from the form
        xsd_file = request.FILES["xsd_file"]
        # read the content of the file
        xsd_data = read_xsd_file(xsd_file)

        template = Template(filename=xsd_file.name, content=xsd_data)
        template_version_manager_api.insert(
            template_version_manager, template, request=request
        )

        # create the fragment url with all the version of the template (minus the new template)
        version_manager_string = ""
        for version in template_version_manager.versions:
            if version != str(template.id):
                current_version_string = (
                    version if version_manager_string == "" else f",{version}"
                )

                version_manager_string += current_version_string

        # add the fragment data to the url
        fragment = f"#from={version_manager_string}&to={template.id}&tvm={template.version_manager.id}"

        return HttpResponseRedirect(
            reverse("core-admin:core_main_app_data_migration") + fragment
        )
    except exceptions.XSDError as xsd_error:
        return handle_xsd_errors(
            request, assets, context, xsd_error, xsd_data, xsd_file.name
        )
    except Exception as exception:
        context["errors"] = html_escape(str(exception))
        return _upload_template_response(request, assets, context)


def _upload_template_response(request, assets, context):
    """Render template upload response.

    Args:
        request:
        context:

    Returns:

    """
    return admin_render(
        request,
        "core_main_app/admin/templates/upload.html",
        assets=assets,
        context=context,
    )


class XSLTView(View):
    """XSLT view."""

    @staticmethod
    @staff_member_required
    def get(request, *args, **kwargs):
        """get request

        Args:
            request:

        Returns:
        """

        modals = [
            EditXSLTView.get_modal_html_path(),
            DeleteObjectModalView.get_modal_html_path(),
        ]

        assets = {
            "js": [
                EditXSLTView.get_modal_js_path(),
                DeleteObjectModalView.get_modal_js_path(),
            ],
        }

        context = {
            "object_name": "XSLT",
            "xslt": xslt_transformation_api.get_all(),
            "update_url": reverse("core-admin:core_main_app_upload_xslt"),
        }

        return admin_render(
            request,
            "core_main_app/admin/xslt/list.html",
            modals=modals,
            assets=assets,
            context=context,
        )


class UploadXSLTView(View):
    """Upload XSLT view."""

    form_class = UploadXSLTForm
    template_name = "core_main_app/admin/xslt/upload.html"
    object_name = "XSLT"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.context.update({"object_name": self.object_name})

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        """get

        Args:
            request:

        Returns:
        """
        self.context.update({"upload_form": self.form_class()})
        return admin_render(request, self.template_name, context=self.context)

    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        """post

        Args:
            request:

        Returns:
        """
        form = self.form_class(request.POST, request.FILES)
        self.context.update({"upload_form": form})

        if form.is_valid():
            return self._save_xslt(request)
        else:
            # Display error from the form
            return admin_render(
                request, self.template_name, context=self.context
            )

    def _save_xslt(self, request):
        """Saves an XSLT.

        Args:
            request: Request.

        """
        try:
            # get the XSLT name
            name = request.POST["name"]
            # get the file from the form
            xsd_file = request.FILES["upload_file"]
            # read the content of the file
            xsd_data = read_xsd_file(xsd_file)
            xslt = XslTransformation(
                name=name, filename=xsd_file.name, content=xsd_data
            )
            xslt_transformation_api.upsert(xslt)

            return HttpResponseRedirect(
                reverse("core-admin:core_main_app_xslt")
            )
        except exceptions.NotUniqueError:
            self.context.update(
                {"errors": html_escape("This name already exists.")}
            )
            return admin_render(
                request,
                "core_main_app/admin/xslt/upload.html",
                context=self.context,
            )
        except Exception as exception:
            self.context.update({"errors": html_escape(str(exception))})
            return admin_render(
                request,
                "core_main_app/admin/xslt/upload.html",
                context=self.context,
            )


def handle_xsd_errors(
    request, assets, context, xsd_error, xsd_content, filename
):
    """Handle XSD errors. Builds dependency resolver if needed.

    Args:
        request:
        assets:
        context:
        xsd_error:
        xsd_content:
        filename:

    Returns:

    """
    imports, includes = get_imports_and_includes(xsd_content)
    # a problem with includes/imports has been detected
    if len(includes) > 0 or len(imports) > 0:
        # build dependency resolver
        context["dependency_resolver"] = get_dependency_resolver_html(
            imports, includes, xsd_content, filename, request=request
        )
        return _upload_template_response(request, assets, context)

    context["errors"] = html_escape(str(xsd_error))
    return _upload_template_response(request, assets, context)


def get_dependency_resolver_html(
    imports, includes, xsd_data, filename, request
):
    """Return HTML for dependency resolver form.

    Args:
        imports:
        includes:
        xsd_data:
        filename:
        request:

    Returns:

    """
    # build the list of dependencies
    current_templates = (
        template_version_manager_api.get_global_version_managers(
            request=request, _cls=False
        )
    )
    list_dependencies_template = loader.get_template(
        "core_main_app/admin/list_dependencies.html"
    )
    context = {
        "templates": [
            template
            for template in current_templates
            if not template.is_disabled
        ],
    }
    list_dependencies_html = list_dependencies_template.render(context)

    # build the dependency resolver form
    dependency_resolver_template = loader.get_template(
        "core_main_app/admin/dependency_resolver.html"
    )
    context = {
        "imports": imports,
        "includes": includes,
        "xsd_content": html_escape(xsd_data),
        "filename": filename,
        "dependencies": list_dependencies_html,
    }
    return dependency_resolver_template.render(context)


class WebPageView(View):
    """Web Page View"""

    form_class = TextAreaForm
    api = None
    get_redirect = None
    post_redirect = None
    web_page_type = None

    @method_decorator(staff_member_required)
    def get(self, request, **kwargs):
        """GET request. Create/Show the form for the configuration.

        Args:
            request:
            **kwargs:

        Returns:

        """
        if "current_content" in kwargs:
            content = kwargs["current_content"]
        else:
            website_object = self.api.get()
            content = (
                website_object.content if website_object is not None else ""
            )

        context = {"form": self.form_class({"content": content})}

        if "error_id" in kwargs:
            if kwargs["error_id"] < len(constants.MARKDOWN_ERRORS):
                context["error_msg"] = constants.MARKDOWN_ERRORS[
                    kwargs["error_id"]
                ]
            else:
                context["error_msg"] = constants.UNKNOWN_ERROR

        assets = {"css": ["core_main_app/admin/css/web_page/style.css"]}

        return admin_render(
            request, self.get_redirect, context=context, assets=assets
        )

    @method_decorator(staff_member_required)
    def post(self, request):
        """POST request. Try to save the configuration.

        Args:
            request:

        Returns:

        """
        form = self.form_class(request.POST)

        if form.is_valid():
            # Call the API
            content = request.POST["content"]
            page = self.api.get()

            markdown_content = markdown(content)
            if markdown_content != stripjs(markdown_content):
                return self.get(
                    request,
                    current_content=content,
                    error_id=constants.MARKDOWN_UNSAFE,
                )

            try:
                parse_html(markdown_content, "div")
            except HTMLError:
                return self.get(
                    request,
                    current_content=content,
                    error_id=constants.MARKDOWN_GENERATION_FAILED,
                )

            if page is None:
                page = WebPage(type=self.web_page_type, content=content)
            else:
                page.content = content

            self.api.upsert(page)
            messages.add_message(
                request, messages.SUCCESS, "Information saved with success."
            )

            return redirect(reverse(self.post_redirect))


@staff_member_required
def data_migration(request):
    """Migrate data to a new template version

    Args:
        request:

    Returns:
    """
    assets = {
        "js": [
            {
                "path": "core_main_app/admin/js/templates/data_migration.raw.js",
                "is_raw": True,
            },
            {
                "path": "core_main_app/admin/js/templates/data_migration.js",
                "is_raw": False,
            },
        ],
        "css": [
            "core_main_app/admin/css/data_migration.css",
            "core_explore_common_app/user/css/toggle.css",
        ],
    }

    # get all current templates
    templates = []
    template_managers = [
        template
        for template in template_version_manager_api.get_global_version_managers(
            request=request
        )
        if not template.is_disabled
    ]

    for template_manager in template_managers:
        version_index = 1
        for version in template_manager.versions:
            templates.append(
                {
                    "id": version,
                    "title": f"{template_manager.title} (version {version_index})",
                }
            )
            version_index += 1

    context = {
        "templates": templates,
        "xslt": xslt_transformation_api.get_all(),
    }

    return admin_render(
        request,
        "core_main_app/admin/templates/data_migration.html",
        assets=assets,
        context=context,
    )


class CustomExceptionReporter(SafeExceptionReporterFilter):
    """Custom view for Django Exception Reports"""

    # hide all settings
    hidden_settings = re.compile(r".*", flags=re.IGNORECASE)
