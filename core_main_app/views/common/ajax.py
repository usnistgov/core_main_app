"""
    Common ajax
"""
import json
from django.http.response import HttpResponse, HttpResponseBadRequest

from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.commons import exceptions


def edit_template_version_manager(request):
    """Edit the template version manager

    Args:
        request:

    Returns:

    """
    title = request.POST['title']
    try:
        template_version_manager = template_version_manager_api.get_by_id(request.POST['id'])
        template_version_manager_api.edit_title(template_version_manager, title)
    except exceptions.NotUniqueError, e:
        return HttpResponseBadRequest("A template called \"" + title + "\" already exists. Please choose another name.")
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def disable_version_manager(request):
    """Disable a version manager

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
    """Restore a disabled version manager

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
    """ Disable a template version of a version manager

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
    """ Disable a version of a version manager

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.disable_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def restore_template_version_from_version_manager(request):
    """ Restore a disabled template version of a version manager

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
    """ Restore a disabled version of a version manager

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.restore_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def set_current_template_version_from_version_manager(request):
    """ Set the current version of a template

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
    """ Set the current version of a version manager

    Args:
        version:

    Returns:

    """
    try:
        version_manager_api.set_current(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

