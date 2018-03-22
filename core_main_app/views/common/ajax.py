"""
    Common ajax
"""
import json

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic.edit import UpdateView

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.views.admin.forms import EditTemplateForm


class EditObjectModalView(UpdateView):
    """ Common EditObjectModalView.
        Should be used with edit.html and edit.js.
    """
    template_name = 'core_main_app/common/commons/edit.html'
    form_class = None
    model = None
    success_url = None
    success_message = None

    def form_invalid(self, form):
        # Get initial response
        response = super(EditObjectModalView, self).form_invalid(form)
        data = {
            'is_valid': False,
            'responseText': response.rendered_content
        }
        return JsonResponse(data)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # Call private save method
        self._save(form)
        if form.is_valid():
            data = {
                'is_valid': True,
                'url': self.get_success_url(),
            }

            if self.success_message:
                messages.success(self.request, self.success_message)

            return JsonResponse(data)
        else:
            return self.form_invalid(form)

    def _save(self, form):
        # Save treatment.
        super(EditObjectModalView, self).form_valid(form)

    @staticmethod
    def get_modal_html_path():
        return "core_main_app/common/modals/edit_page_modal.html"

    @staticmethod
    def get_modal_js_path():
        return {"path": 'core_main_app/common/js/modals/edit.js', "is_raw": False}


class EditTemplateVersionManagerView(EditObjectModalView):
    form_class = EditTemplateForm
    model = TemplateVersionManager
    success_url = reverse_lazy("admin:core_main_app_templates")
    success_message = 'Name edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            template_version_manager_api.edit_title(self.object, form.cleaned_data.get('title'))
        except exceptions.NotUniqueError:
            form.add_error(None, "An object with the same name already exists. Please choose "
                                 "another name.")
        except Exception, e:
            form.add_error(None, e.message)


def disable_version_manager(request):
    """Disable a version manager.

    Args:
        request:

    Returns:

    """
    try:
        version_manager = version_manager_api.get(request.GET['id'])
        version_manager_api.disable(version_manager)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def restore_version_manager(request):
    """Restore a disabled version manager.

    Args:
        request:

    Returns:

    """
    try:
        version_manager = version_manager_api.get(request.GET['id'])
        version_manager_api.restore(version_manager)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def disable_template_version_from_version_manager(request):
    """ Disable a template version of a version manager.

    Args:
        request:

    Returns:

    """
    try:
        disable_version_of_version_manager(template_api.get(request.GET['id']))
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def disable_version_of_version_manager(version):
    """ Disable a version of a version manager.

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.disable_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def restore_template_version_from_version_manager(request):
    """ Restore a disabled template version of a version manager.

    Args:
        request:

    Returns:

    """
    try:
        restore_version_from_version_manager(template_api.get(request.GET['id']))
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def restore_version_from_version_manager(version):
    """ Restore a disabled version of a version manager.

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.restore_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def set_current_template_version_from_version_manager(request):
    """ Set the current version of a template.

    Args:
        request:

    Returns:

    """
    try:
        set_current_version_from_version_manager(template_api.get(request.GET['id']))
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def set_current_version_from_version_manager(version):
    """ Set the current version of a version manager.

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.set_current(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

