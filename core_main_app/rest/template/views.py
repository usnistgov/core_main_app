"""REST views for the template API
"""
from io import StringIO
import json

from django.http.response import HttpResponse
from rest_framework.decorators import api_view

from core_main_app.commons import exceptions as exceptions
from core_main_app.commons.exceptions import RestApiError
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager import api as template_version_manager_api
from rest_framework.response import Response
from rest_framework import status

from core_main_app.components.template.api import init_template_with_dependencies
from core_main_app.rest.serializers import CreateTemplateSerializer, CreateTemplateVersionManagerSerializer, \
    TemplateSerializer
from core_main_app.utils.file import get_file_http_response


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
    template_object = _get_template(template_id)

    try:
        return get_file_http_response(template_object.content, template_object.filename, 'text/xsd', 'xsd')
    except Exception, e:
        content = {'message': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_by_id(request):
    """GET /rest/template?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        template_id = request.query_params.get('id', None)

        # Check parameters
        if template_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        template_object = _get_template(template_id)

        # Serialize object
        template_serializer = TemplateSerializer(template_object)
        # Return response
        return Response(template_serializer.data, status=status.HTTP_200_OK)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _post(request):
    """ POST /rest/template
    {
    "filename": "filename",
    "title": "title",
    "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'/></xs:schema>"
    }

    Note: "dependencies"= json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

    Args:
        request:

    Returns:

    """
    try:
        # Build serializers
        create_template_serializer = CreateTemplateSerializer(data=request.data)
        create_template_version_manager_serializer = CreateTemplateVersionManagerSerializer(data=request.data)

        # Validate data
        create_template_serializer.is_valid(True)
        create_template_version_manager_serializer.is_valid(True)

        # Deserialize object
        template_object = create_template_serializer.create(create_template_serializer.data)
        template_version_manager_object = create_template_version_manager_serializer.create(
            create_template_version_manager_serializer.data)

        # Get template parameters
        dependencies = request.data.get('dependencies', None)

        # If dependencies, load the dict from json
        dependencies_dict = _load_dependencies(dependencies)

        # Update the content of the template with dependencies
        init_template_with_dependencies(template_object, dependencies_dict)

        # Create the template and its template version manager
        template_version_manager_api.insert(template_version_manager_object, template_object)

        # Returns the serialized template
        template_serializer = TemplateSerializer(template_object)
        return Response(template_serializer.data, status=status.HTTP_201_CREATED)
    except Exception as api_exception:
        content = {'message': api_exception.message} # TODO: test not api_exception.details
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def template(request):
    """Template api

    Args:
        request:

    Returns:

    """
    if request.method == 'POST':
        return _post(request)


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


def _load_dependencies(dependencies=None):
    """Returns dependencies as a dict

    Args:
        dependencies:

    Returns:

    """
    if dependencies is not None:
        try:
            return json.loads(dependencies)
        except:
            raise RestApiError('Incorrect format of the dependencies parameter.')
    return None
