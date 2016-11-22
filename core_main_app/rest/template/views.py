"""REST views for the template API
"""
from io import StringIO

from django.http.response import HttpResponse
from rest_framework.decorators import api_view

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def download(request):
    """Downloads the template file

    Args:
        request:

    Returns:

    """
    # Get parameters
    template_id = request.query_params.get('id', None)

    # Check parameters

    if template_id is None:
        content = {'message': 'Expected parameters not provided.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Get template from id
    template = _get_template(template_id)
    return _get_file_response(template)


def _get_template(template_id):
    """Get a template by its id

    Args:
        template_id:

    Returns:

    """
    try:
        return template_api.get(template_id)
    except exceptions.DoesNotExist:
        content = {'message': 'No template could be found with the given id.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception, e:
        # TODO: log e.message
        content = {'message': 'An unexpected error happened.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_file_response(template):
    """Get an HTTP response with the file

    Args:
        template:

    Returns:

    """
    try:
        # Get template content
        xsd_content = template.content
        # Set file content
        xsd_file = StringIO(xsd_content)
        response = HttpResponse(xsd_file, content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=' + template.filename
        return response
    except Exception, e:
        # TODO: log e.message
        content = {'message': 'An unexpected error happened.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
