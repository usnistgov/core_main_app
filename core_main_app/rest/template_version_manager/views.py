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
    """Return a template version manager by its id.

    GET /rest/template-version-manager?id=<id>

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
        template_version_manager_object = version_manager_api.get(template_version_manager_id)
        # Serialize object
        template_version_manager_serializer = TemplateVersionManagerSerializer(template_version_manager_object)
        # Return response
        return Response(template_version_manager_serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'No template version manager could be found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_globals(request):
    """Return http response with all global template version managers.

    GET /rest/template-version-manager/get/all/global

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


@api_view(['GET'])
def get_active_by_user(request):
    """Return http response with all active template version managers of a user.

    GET /rest/template-version-manager/get/active/user

    Args:
        request:

    Returns:

    """
    try:
        template_version_managers = template_version_manager_api.\
            get_active_version_manager_by_user_id(user_id=request.user.id)
        template_version_manager_serializer = TemplateVersionManagerSerializer(template_version_managers, many=True)
        return Response(template_version_manager_serializer.data, status=status.HTTP_200_OK)
    except Exception, e:
        content = {'message:': e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
