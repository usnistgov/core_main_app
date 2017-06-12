"""Admin AJAX views
"""
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_main_app.components.template.api import init_template_with_dependencies
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.commons.exceptions import NotUniqueError
import HTMLParser


def resolve_dependencies(request):
    """Resolve import/includes to avoid local references.

    Args:
        request:

    Returns:

    """
    try:
        # Get the parameters
        name = request.POST.get('name', None)
        version_manager_id = request.POST.get('version_manager_id', '')
        filename = request.POST['filename']
        xsd_content = request.POST['xsd_content']
        schema_locations = request.POST.getlist('schemaLocations[]')
        dependencies = request.POST.getlist('dependencies[]')

        # create new object
        template = Template(filename=filename, content=_get_xsd_content_from_html(xsd_content))
        init_template_with_dependencies(template, _get_dependencies_dict(schema_locations, dependencies))

        # get the version manager or create a new one
        if version_manager_id != '':
            template_version_manager = version_manager_api.get(version_manager_id)
        else:
            template_version_manager = TemplateVersionManager(title=name)
        template_version_manager_api.insert(template_version_manager, template)
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def _get_dependencies_dict(schema_locations, dependencies):
    """Build a dict from lists of schema locations and dependencies.

    Args:
        schema_locations:
        dependencies:

    Returns:

    """
    string_to_python_dependencies = []
    # transform 'None' into python None
    for dependency in dependencies:
        if dependency == 'None':
            string_to_python_dependencies.append(None)
        else:
            string_to_python_dependencies.append(dependency)
    return dict(zip(schema_locations, string_to_python_dependencies))


def _get_xsd_content_from_html(xsd_content):
    """Decode XSD content from HTML.

    Args:
        xsd_content:

    Returns:

    """
    html_parser = HTMLParser.HTMLParser()
    xsd_content = str(html_parser.unescape(xsd_content).encode("utf-8"))
    return xsd_content


def edit_xslt_name(request):
    """Edit the xslt.

    Args:
        request:

    Returns:

    """
    try:
        xslt = xsl_transformation_api.get_by_id(request.POST['id'])
        name = request.POST['name']
        xslt.name = name
        xsl_transformation_api.upsert(xslt)
    except NotUniqueError:
        return HttpResponseBadRequest("Name already exists.")
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def delete_xslt(request):
    """Delete the xslt.

    Args:
        request:

    Returns:

    """
    try:
        xslt = xsl_transformation_api.get_by_id(request.POST['id'])
        xsl_transformation_api.delete(xslt)
    except Exception, e:
        return HttpResponseBadRequest(e.message)

    return HttpResponse(json.dumps({}), content_type='application/javascript')
