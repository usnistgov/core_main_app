"""
    Common views
"""
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.html import escape as html_escape
from django.views.generic import View

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template_xsl_rendering import api as template_xsl_rendering_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.xsl_transformation import api as xslt_transformation_api
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils.rendering import render
from core_main_app.views.admin.forms import UploadXSLTForm, TemplateXsltRenderingForm


class XSLTView(View):
    """
    Class' purpose: XSLT view.
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
    """Returns the content of the file uploaded using Django FileField

    Returns:

    """
    # put the cursor at the beginning of the file
    xsd_file.seek(0)
    # read the content of the file
    return xsd_file.read()


class UploadXSLTView(View):
    """
    Class' purpose: Upload XSLT view.
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
        """Saves an XSLT.

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
        except Exception, e:
            self.context.update({'errors': html_escape(e.message)})
            return render(request, 'core_main_app/common/xslt/upload.html', context=self.context)


class TemplateXSLRenderingView(View):
    """
    Class' purpose: Template XSL rendering view.
    """
    form_class = TemplateXsltRenderingForm
    template_name = "core_main_app/common/templates_xslt/main.html"
    context = {}
    assets = {
        "js": [
            {
                "path": 'core_main_app/common/js/backtoprevious.js',
                "is_raw": True
            }
        ]
    }

    def get(self, request, *args, **kwargs):
        """ GET request. Creates/Shows the form for the configuration.

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

        self.context = {
            'template_title': version_manager.title,
            'template_version': version_number,
            "form_template_xsl_rendering": self.form_class(data)
        }

        return render(request, self.template_name, context=self.context, assets=self.assets)

    def post(self, request, *args, **kwargs):
        """ POST request. Try to saves the configuration.

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
            return render(request, self.template_name, context=self.context)

    def _save_template_xslt(self, request):
        """Saves a template xslt rendering.

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

            #TODO: user dashboard installed go to template page, home otherwise
            return HttpResponseRedirect(reverse("core_main_app_templates"))
        except Exception, e:
            self.context.update({'errors': html_escape(e.message)})
            return render(request, self.template_name, context=self.context)
