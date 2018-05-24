""" REST views for the workspace API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

import core_main_app.components.workspace.api as workspace_api
import core_main_app.components.user.api as user_api
import core_main_app.components.group.api as group_api
from core_main_app.commons import exceptions
from core_main_app.rest.workspace.serializers import WorkspaceSerializer
from core_main_app.rest.user.serializers import UserSerializer
from core_main_app.rest.group.serializers import GroupSerializer
from core_main_app.utils.access_control.exceptions import AccessControlError


class WorkspaceList(APIView):
    """ List all user workspace, or create a new one.
    """

    def get(self, request):
        """ Get all user workspaces.

        Args:
            request:

        Returns:

        """
        try:
            if request.user.is_superuser:
                workspace_list = workspace_api.get_all()
            else:
                workspace_list = workspace_api.get_all_by_owner(request.user)

            # Serialize object
            serializer = WorkspaceSerializer(workspace_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """ Create workspace.

        Args:
            request:

        Returns:

        """
        try:
            # Build serializer
            serializer = WorkspaceSerializer(data=request.data)

            # Validate data
            serializer.is_valid(True)

            # Save data
            serializer.save()

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as validation_exception:
            content = {'message': validation_exception}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkspaceDetail(APIView):
    """ Workspace Detail.
    """

    def get(self, request, pk):
        """ Retrieve workspace

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            workspace_object = workspace_api.get_by_id(pk)

            # Serialize object
            serializer = WorkspaceSerializer(workspace_object)

            # Return response
            return Response(serializer.data)
        except exceptions.DoesNotExist:
            content = {'message': 'Workspace not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete a workspace

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            workspace_object = workspace_api.get_by_id(pk)

            # delete object
            workspace_api.delete(workspace_object, request.user)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = {'message': 'Workspace not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {'message': ace.message}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_workspaces_with_read_access(request):
    """ Get all workspaces with read access.

        /rest/workspace/read_access

        Args:
            request:

        Returns:

    """
    return _list_of_workspaces_to_response(workspace_api.get_all_workspaces_with_read_access_by_user(request.user))


@api_view(['GET'])
def get_workspaces_with_write_access(request):
    """ Get all workspaces with write access.

        /rest/workspace/write_access

        Args:
            request:

        Returns:

    """
    return _list_of_workspaces_to_response(workspace_api.get_all_workspaces_with_write_access_by_user(request.user))


def _list_of_workspaces_to_response(func):
    """ Serialize and generate response the list of workspaces you can get with func method.

        Args:
            func:

        Returns:
    """
    try:
        # Get object list
        workspace_object_list = func

        # Serialize object
        return_value = WorkspaceSerializer(workspace_object_list, many=True)

        # Return response
        return Response(return_value.data, status=status.HTTP_200_OK)

    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def is_workspace_public(request, pk):
    """ Is the workspace public.

        Args:
            request:
            pk:

        Returns:

    """
    try:
        # Get object
        workspace_object = workspace_api.get_by_id(pk)

        # Return response
        return Response(workspace_api.is_workspace_public(workspace_object), status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'Workspace not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def set_workspace_public(request, pk):
    """ Set the workspace public.

        Args:
            request:
            pk:

        Returns:

    """
    try:
        # Get object
        workspace_object = workspace_api.get_by_id(pk)

        # Set the workspace public
        workspace_api.set_workspace_public(workspace_object, request.user)

        # Return response
        return Response(status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = {'message': 'Workspace not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except AccessControlError as ace:
        content = {'message': ace.message}
        return Response(content, status=status.HTTP_403_FORBIDDEN)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_list_user_can_write_workspace(request, pk):
    """ Get list of users that have write access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_user_can_write_workspace,
                                                request.user, UserSerializer)


@api_view(['GET'])
def get_list_user_can_read_workspace(request, pk):
    """ Get list of users that have read access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_user_can_read_workspace,
                                                request.user, UserSerializer)


@api_view(['GET'])
def get_list_user_can_access_workspace(request, pk):
    """ Get list of users that have read or write access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_user_can_access_workspace,
                                                request.user, UserSerializer)


@api_view(['GET'])
def get_list_group_can_write_workspace(request, pk):
    """ Get list of groups that have write access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_group_can_write_workspace,
                                                request.user, GroupSerializer)


@api_view(['GET'])
def get_list_group_can_read_workspace(request, pk):
    """ Get list of groups that have read access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_group_can_read_workspace,
                                                request.user, GroupSerializer)


@api_view(['GET'])
def get_list_group_can_access_workspace(request, pk):
    """ Get list of groups that have read or write access to workspace.

    Args:
        request:
        pk:

    Returns:

    """
    return _list_of_users_or_groups_to_response(pk, workspace_api.get_list_group_can_access_workspace,
                                                request.user, GroupSerializer)


def _list_of_users_or_groups_to_response(pk, func, user, serializer):
    """ List of users or groups to response.

    Args:
        pk:
        func:
        user:

    Returns:

    """
    try:
        # Get object
        workspace_object = workspace_api.get_by_id(pk)

        # Get list User
        list_user = func(workspace_object, user)

        # Serialize object
        serializer = serializer(list_user, many=True)

        # Return response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except exceptions.DoesNotExist:
        content = {'message': 'Workspace not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except AccessControlError as ace:
        content = {'message': ace.message}
        return Response(content, status=status.HTTP_403_FORBIDDEN)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _add_or_remove_to_user_or_group_right_to_workspace(request, pk, user_or_group_id, func, get_group_or_user_func):
    """ Add

    Args:
        request:
        pk:
        user_or_group_id:
        func:
        get_group_or_user_func

    Returns:
    """

    try:
        # Get object
        workspace_object = workspace_api.get_by_id(pk)

        # Get user
        user_or_group = get_group_or_user_func(user_or_group_id)

        # Add right
        func(workspace_object, user_or_group, request.user)

        # Return response
        return Response(status=status.HTTP_200_OK)

    except exceptions.DoesNotExist:
        content = {'message': 'Workspace not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except AccessControlError as ace:
        content = {'message': ace.message}
        return Response(content, status=status.HTTP_403_FORBIDDEN)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def add_user_read_right_to_workspace(request, pk, user_id):
    """ Add to the user the read right to the workspace.

    Args:
        request:
        pk:
        user_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, user_id,
                                                              workspace_api.add_user_read_access_to_workspace,
                                                              user_api.get_user_by_id)


@api_view(['PATCH'])
def add_user_write_right_to_workspace(request, pk, user_id):
    """ Add to the user the write right to the workspace.

    Args:
        request:
        pk:
        user_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, user_id,
                                                              workspace_api.add_user_write_access_to_workspace,
                                                              user_api.get_user_by_id)


@api_view(['PATCH'])
def add_group_read_right_to_workspace(request, pk, group_id):
    """ Add to the group the read right to the workspace.

    Args:
        request:
        pk:
        group_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, group_id,
                                                              workspace_api.add_group_read_access_to_workspace,
                                                              group_api.get_group_by_id)


@api_view(['PATCH'])
def add_group_write_right_to_workspace(request, pk, group_id):
    """ Add to the group the write right to the workspace.

    Args:
        request:
        pk:
        group_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, group_id,
                                                              workspace_api.add_group_write_access_to_workspace,
                                                              group_api.get_group_by_id)


@api_view(['PATCH'])
def remove_user_read_right_to_workspace(request, pk, user_id):
    """ Remove from the user the read right to the workspace.

    Args:
        request:
        pk:
        user_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, user_id,
                                                              workspace_api.remove_user_read_access_to_workspace,
                                                              user_api.get_user_by_id)


@api_view(['PATCH'])
def remove_user_write_right_to_workspace(request, pk, user_id):
    """ Remove from the user the write right to the workspace.

    Args:
        request:
        pk:
        user_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, user_id,
                                                              workspace_api.remove_user_write_access_to_workspace,
                                                              user_api.get_user_by_id)


@api_view(['PATCH'])
def remove_group_read_right_to_workspace(request, pk, group_id):
    """ Remove from the group the read right to the workspace.

    Args:
        request:
        pk:
        group_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, group_id,
                                                              workspace_api.remove_group_read_access_to_workspace,
                                                              group_api.get_group_by_id)


@api_view(['PATCH'])
def remove_group_write_right_to_workspace(request, pk, group_id):
    """ Remove from the group the write right to the workspace.

    Args:
        request:
        pk:
        group_id:

    Returns:

    """
    return _add_or_remove_to_user_or_group_right_to_workspace(request, pk, group_id,
                                                              workspace_api.remove_group_write_access_to_workspace,
                                                              group_api.get_group_by_id)


