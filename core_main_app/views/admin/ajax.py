import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.utils.xml import get_template_with_server_dependencies
import HTMLParser


def disable_template(request):
    """
    Disables a template
    :param request:
    :return:
    """
    try:
        version_manager = version_manager_api.get(request.GET['id'])
        version_manager_api.disable(version_manager)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def restore_template(request):
    """
    Restores a disabled template
    :param request:
    :return:
    """
    try:
        version_manager = version_manager_api.get(request.GET['id'])
        version_manager_api.restore(version_manager)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def disable_template_version(request):
    """
    Disables a version of a template
    :param request:
    :return:
    """
    try:
        version = template_api.get(request.GET['id'])
        version_manager_api.disable_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def restore_template_version(request):
    """
    Restores a disabled version of a template
    :param request:
    :return:
    """
    try:
        version = template_api.get(request.GET['id'])
        version_manager_api.restore_version(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def set_current_version(request):
    """
    Sets the current version of a template
    :param request:
    :return:
    """
    try:
        version = template_api.get(request.GET['id'])
        version_manager_api.set_current(version)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_template(request):
    """
    Edit the template
    :param request:
    :return:
    """
    try:
        version_manager = version_manager_api.get(request.GET['id'])
        version_manager.title = request.GET['title']
        version_manager_api.upsert(version_manager)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def resolve_dependencies(request):
    """
    Resolve import/includes to avoid local references
    :param request:
    :return:
    """
    try:
        # Get the parameters
        name = request.POST.get('name', None)
        version_manager_id = request.POST.get('version_manager_id', '')
        filename = request.POST['filename']
        xsd_content = request.POST['xsd_content']
        schema_locations = request.POST.getlist('schemaLocations[]')
        dependencies = request.POST.getlist('dependencies[]')

        # Update the XSD content with chosen dependencies
        updated_xsd_content = _update_template_dependencies(xsd_content, schema_locations, dependencies)

        # create new object
        template = Template(filename=filename, content=updated_xsd_content, dependencies=dependencies)
        # get the version manager or create a new one
        if version_manager_id != '':
            template_version_manager = version_manager_api.get(version_manager_id)
        else:
            template_version_manager = TemplateVersionManager(title=name)
        template_version_manager_api.insert(template_version_manager, template)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _get_dependencies_dict(schema_locations, dependencies):
    """
    Build a dict from lists got from the AJAX
    :param schema_locations:
    :param dependencies:
    :return:
    """
    string_to_python_dependencies = []
    # transform 'None' into python None
    for dependency in dependencies:
        if dependency == 'None':
            string_to_python_dependencies.append(None)
        else:
            string_to_python_dependencies.append(dependency)
    return dict(zip(schema_locations, string_to_python_dependencies))


def _update_template_dependencies(xsd_content, schema_locations, dependencies):
    """

    Args:
        xsd_content:
        schema_locations:
        dependencies:

    Returns:

    """
    html_parser = HTMLParser.HTMLParser()
    xsd_content = str(html_parser.unescape(xsd_content))
    dependencies_dict = _get_dependencies_dict(schema_locations, dependencies)
    return get_template_with_server_dependencies(xsd_content, dependencies_dict)
