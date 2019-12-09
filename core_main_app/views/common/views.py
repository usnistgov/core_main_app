"""
    Common views
"""
from abc import ABCMeta

from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http.response import HttpResponseRedirect
from django.utils.html import escape as html_escape
from django.views.generic import View

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data import api as data_api
from core_main_app.components.group import api as group_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering import api as template_xsl_rendering_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.xsl_transformation import api as xslt_transformation_api
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils import group as group_utils
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.rendering import admin_render
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import UploadXSLTForm, TemplateXsltRenderingForm


class CommonView(View, metaclass=ABCMeta):
    """
        Abstract common view for admin and user.
    """

    administration = False

    def common_render(self, request, template_name, modals=None, assets=None, context=None):
        return admin_render(request, template_name, modals, assets, context) if self.administration \
            else render(request, template_name, modals, assets, context)


class EditWorkspaceRights(CommonView):
    """
        Edit workspace rights
    """

    template = "core_main_app/user/workspaces/edit_rights.html"

    def get(self, request, *args, **kwargs):

        try:
            workspace_id = kwargs['workspace_id']
            workspace = workspace_api.get_by_id(workspace_id)
        except DoesNotExist as e:
            return HttpResponseBadRequest("The workspace does not exist.")
        except:
            return HttpResponseBadRequest("Something wrong happened.")

        if workspace.owner != str(request.user.id) and not self.administration:
            return HttpResponseForbidden("Only the workspace owner can edit the rights.")

        try:
            # Users
            users_read_workspace = workspace_api.get_list_user_can_read_workspace(workspace, request.user)
            users_write_workspace = workspace_api.get_list_user_can_write_workspace(workspace, request.user)

            users_access_workspace = list(set(users_read_workspace + users_write_workspace))
            detailed_users = []
            for user in users_access_workspace:
                if str(user.id) != workspace.owner:
                    detailed_users.append({'object_id': user.id,
                                           'object_name': user.username,
                                           'can_read': user in users_read_workspace,
                                           'can_write': user in users_write_workspace,
                                           })
        except:
            detailed_users = []

        try:
            # Groups
            groups_read_workspace = workspace_api.get_list_group_can_read_workspace(workspace, request.user)
            groups_write_workspace = workspace_api.get_list_group_can_write_workspace(workspace, request.user)

            groups_access_workspace = list(set(groups_read_workspace + groups_write_workspace))
            group_utils.remove_list_object_from_list(groups_access_workspace,
                                                     [group_api.get_anonymous_group(), group_api.get_default_group()])
            detailed_groups = []
            for group in groups_access_workspace:
                detailed_groups.append({'object_id': group.id,
                                        'object_name': group.name,
                                        'can_read': group in groups_read_workspace,
                                        'can_write': group in groups_write_workspace,
                                        })
        except:
            detailed_groups = []

        context = {
            'workspace': workspace,
            'user_data': detailed_users,
            'group_data': detailed_groups,
            'template': "core_main_app/user/workspaces/list/edit_rights_table.html",
            'action_read': 'action_read',
            'action_write': 'action_write',
            'user': 'user',
            'group': 'group',
        }

        if workspace_api.is_workspace_public(workspace):
            context.update({'is_public': True})
        if workspace_api.is_workspace_global(workspace):
            context.update({'is_global': True})

        assets = {
            "css": ['core_main_app/libs/datatables/1.10.13/css/jquery.dataTables.css',
                    'core_main_app/libs/fSelect/css/fSelect.css',
                    'core_main_app/common/css/switch.css'],

            "js": [{
                    "path": 'core_main_app/libs/datatables/1.10.13/js/jquery.dataTables.js',
                    "is_raw": True
                },
                {
                    "path": "core_main_app/libs/fSelect/js/fSelect.js",
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/common/js/backtoprevious.js',
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/user/js/workspaces/tables.js',
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/user/js/workspaces/add_user.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/list/modals/switch_right.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/list/modals/remove_rights.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/add_group.js',
                    "is_raw": False
                },
                {
                    "path": 'core_main_app/user/js/workspaces/init.js',
                    "is_raw": False
                }]
        }

        modals = ["core_main_app/user/workspaces/list/modals/add_user.html",
                  "core_main_app/user/workspaces/list/modals/switch_right.html",
                  "core_main_app/user/workspaces/list/modals/remove_rights.html",
                  "core_main_app/user/workspaces/list/modals/add_group.html"]

        return self.common_render(request, self.template,
                                  context=context,
                                  assets=assets,
                                  modals=modals)


class ViewData(CommonView):
    """
        View detail data.
    """
    template = 'core_main_app/user/data/detail.html'

    def get(self, request, *args, **kwargs):
        data_id = request.GET['id']

        try:
            data = data_api.get_by_id(data_id, request.user)

            context = {
                'data': data
            }

            assets = {
                "js": [
                    {
                        "path": 'core_main_app/common/js/XMLTree.js',
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/user/js/data/detail.js',
                        "is_raw": False
                    },
                ],
                "css": ["core_main_app/common/css/XMLTree.css"],
            }

            modals = []

            if "core_file_preview_app" in INSTALLED_APPS:
                assets["js"].extend([
                    {
                        "path": 'core_file_preview_app/user/js/file_preview.js',
                        "is_raw": False
                    }
                ])
                assets["css"].append("core_file_preview_app/user/css/file_preview.css")
                modals.append("core_file_preview_app/user/file_preview_modal.html")

            return self.common_render(request, self.template, context=context, assets=assets, modals=modals)
        except exceptions.DoesNotExist:
            error_message = 'Data not found'
        except exceptions.ModelError:
            error_message = 'Model error'
        except Exception as e:
            error_message = str(e)

        return self.common_render(request, 'core_main_app/common/commons/error.html',
                                  context={"error": "Unable to access the requested " + get_data_label() + ": {}.".format(error_message)})


class XSLTView(View):
    """XSLT view.
    """

    @staticmethod
    def get(request, *args, **kwargs):
        modals = [
            "core_main_app/common/xslt/list/modals/edit.html",
            "core_main_app/common/xslt/list/modals/delete.html"
        ]

        assets = {
            "js": [
                {
                    "path": "core_main_app/common/js/xslt/list/modals/edit.js",
                    "is_raw": False
                },
                {
                    "path": "core_main_app/common/js/xslt/list/modals/delete.js",
                    "is_raw": False
                }
            ],
        }

        context = {
            'object_name': 'XSLT',
            "xslt": xslt_transformation_api.get_all(),
            "update_url": reverse('core_main_app_upload_xslt')
        }

        return render(request, "core_main_app/common/xslt/list.html", modals=modals, assets=assets,
                      context=context)


def read_xsd_file(xsd_file):
    """Return the content of the file uploaded using Django FileField.

    Returns:

    """
    # put the cursor at the beginning of the file
    xsd_file.seek(0)
    # read the content of the file
    return xsd_file.read().decode('utf-8')


class UploadXSLTView(View):
    """Upload XSLT view.
    """
    form_class = UploadXSLTForm
    template_name = 'core_main_app/common/xslt/upload.html'
    object_name = 'XSLT'

    def __init__(self, **kwargs):
        super(UploadXSLTView, self).__init__(**kwargs)
        self.context = {}
        self.context.update({'object_name': self.object_name})

    def get(self, request, *args, **kwargs):
        self.context.update({'upload_form': self.form_class()})
        return render(request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        self.context.update({'upload_form': form})

        if form.is_valid():
            return self._save_xslt(request)
        else:
            # Display error from the form
            return render(request, self.template_name, context=self.context)

    def _save_xslt(self, request):
        """Save an XSLT.

        Args:
            request: Request.

        """
        try:
            # get the XSLT name
            name = request.POST['name']
            # get the file from the form
            xsd_file = request.FILES['upload_file']
            # read the content of the file
            xsd_data = read_xsd_file(xsd_file)
            xslt = XslTransformation(name=name, filename=xsd_file.name, content=xsd_data)
            xslt_transformation_api.upsert(xslt)

            return HttpResponseRedirect(reverse("core_main_app_xslt"))
        except Exception as e:
            self.context.update({'errors': html_escape(str(e))})
            return render(request, 'core_main_app/common/xslt/upload.html', context=self.context)


class TemplateXSLRenderingView(View):
    """Template XSL rendering view.
    """
    rendering = render
    save_redirect = "core_main_app_manage_template_versions"
    back_to_url = "core_main_app_manage_template_versions"
    form_class = TemplateXsltRenderingForm
    template_name = "core_main_app/common/templates_xslt/main.html"
    context = {}
    assets = {}

    def get(self, request, *args, **kwargs):
        """ GET request. Create/Show the form for the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        template_id = kwargs.pop('template_id')
        # Get the template
        template = template_api.get(template_id)
        # Get template information (version)
        version_manager = version_manager_api.get_from_version(template)
        version_number = version_manager_api.get_version_number(version_manager, template_id)
        try:
            # Get the existing configuration to build the form
            template_xsl_rendering = template_xsl_rendering_api.get_by_template_id(template_id)
            data = {'id': template_xsl_rendering.id, 'template': template.id,
                    'list_xslt': template_xsl_rendering.list_xslt.id if template_xsl_rendering.list_xslt else None,
                    'detail_xslt': template_xsl_rendering.detail_xslt.id if template_xsl_rendering.detail_xslt else None
                   }
        except (Exception, exceptions.DoesNotExist):
            # If no configuration, new form with pre-selected fields.
            data = {'template': template.id, 'list_xslt': None, 'detail_xslt': None}

        self.assets = {
            "css": ['core_main_app/admin/css/templates_xslt/form.css'],
        }

        self.context = {
            'template_title': version_manager.title,
            'template_version': version_number,
            "form_template_xsl_rendering": self.form_class(data),
            'url_back_to': reverse(self.back_to_url, kwargs={'version_manager_id': version_manager.id})
        }

        return self.rendering(request, self.template_name, context=self.context, assets=self.assets)

    def post(self, request, *args, **kwargs):
        """ POST request. Try to save the configuration.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """
        form = self.form_class(request.POST, request.FILES)
        self.context.update({'form_template_xsl_rendering': form})

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
                list_xslt = xslt_transformation_api.get_by_id(request.POST.get('list_xslt'))
            except (Exception, exceptions.DoesNotExist):
                list_xslt = None
            # Get the detail xslt instance
            try:
                detail_xslt = xslt_transformation_api.get_by_id(request.POST.get('detail_xslt'))
            except (Exception, exceptions.DoesNotExist):
                detail_xslt = None

            template_xsl_rendering_api.add_or_delete(template_xsl_rendering_id=request.POST.get('id'),
                                                     template_id=request.POST.get('template'),
                                                     list_xslt=list_xslt, detail_xslt=detail_xslt)

            template = template_api.get(request.POST.get('template'))
            # Get template information (version)
            version_manager = version_manager_api.get_from_version(template)
            return HttpResponseRedirect(reverse(self.save_redirect, args=[version_manager.id]))
        except Exception as e:
            self.context.update({'errors': html_escape(str(e))})
            return self.rendering(request, self.template_name, context=self.context)


def defender_error_page(request):
    """ Error page for defender package.

    Args:
        request:

    Returns:

    """
    return render(request, "core_main_app/common/defender/error.html")
