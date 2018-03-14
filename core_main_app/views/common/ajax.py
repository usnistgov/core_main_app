"""
    Common ajax
"""
import json

from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        redirect_url = self._save(form)

        return redirect_url

    def _save(self, form):
        # Save treatment.
        # It should return an HttpResponse.
        return super(EditObjectModalView, self).form_valid(form)

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

    def _save(self, form):
        # Save treatment.
        # It should return an HttpResponse.
        try:
            template_version_manager_api.edit_title(self.object, form.cleaned_data.get('title'))
            messages.add_message(self.request, messages.SUCCESS, 'Name edited with success.')
        except exceptions.NotUniqueError:
            form.add_error(None, "An object with the same name already exists. Please choose "
                                 "another name.")
            return super(EditTemplateVersionManagerView, self).form_invalid(form)
        except Exception, e:
            form.add_error(None, e.message)
            return super(EditTemplateVersionManagerView, self).form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())


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

