"""REST views for the template version manager API
"""
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.rest.serializers import TemplateVersionManagerSerializer
from core_main_app.commons import exceptions as exceptions


@api_view(['GET'])
def get_by_id(request):
    """GET /rest/template-version-manager?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        template_version_manager_id = request.query_params.get('id', None)

        # Check parameters
        if template_version_manager_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get object
        template_version_manager_object = _get_template_version_manager(template_version_manager_id)
        # Serialize object
        template_version_manager_serializer = TemplateVersionManagerSerializer(template_version_manager_object)
        # Return response
        return Response(template_version_manager_serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def template_version_manager(request):
    """Template version manager api

    Args:
        request:

    Returns:

    """
    if request.method == 'GET':
        return get_by_id(request)


@api_view(['GET'])
def get_all_globals(request):
    """GET /rest/template-version-manager/select/all/global

    Args:
        request:

    Returns:

    """
    try:
        template_version_managers = template_version_manager_api.get_global_version_managers()
        template_version_manager_serializer = TemplateVersionManagerSerializer(template_version_managers, many=True)
        return Response(template_version_manager_serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_template_version_manager(template_version_manager_id):
    """Get a template version manager by its id

    Args:
        template_version_manager_id:

    Returns:

    """
    try:
        return version_manager_api.get(template_version_manager_id)
    except exceptions.DoesNotExist:
        content = {'message': 'No template version manager could be found with the given id.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception, e:
        # TODO: log e.message
        content = {'message': 'An unexpected error happened.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)