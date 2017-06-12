""" REST views for the blob API
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core_main_app.commons import exceptions
import core_main_app.components.blob.api as blob_api
from core_main_app.components.blob.utils import get_blob_download_uri
from core_main_app.utils.file import get_file_http_response
from core_main_app.rest.blob import serializers
from core_main_app.components.user import api as user_api


@api_view(['GET'])
def download(request):
    """Download the blob file.

    /rest/blob/download?id=<id>

    Args:
        request:

    Returns:

    """
    try:
        # Get parameters
        blob_id = request.query_params.get('id', None)

        # Check parameters
        if blob_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get template from id
        blob_object = blob_api.get_by_id(blob_id)

        return get_file_http_response(blob_object.blob, blob_object.filename)
    except exceptions.DoesNotExist as e:
        content = {'message': 'No blob found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete(request):
    """ Delete a given blob.

    DELETE http://<server_ip>:<server_port>/<rest_main>/blob/delete?id=id

    Args:
        request (HttpRequest): request.

    Returns:
        Response object

    """
    try:
        # Get parameters
        blob_id = request.query_params.get('id', None)

        # Check parameters
        if blob_id is None:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # Get blob
        blob_object = blob_api.get_by_id(blob_id)
        # Check rights
        if str(request.user.id) == blob_object.user_id or request.user.is_staff:
            # Delete blob
            message, status_code = _delete_blob(blob_object)
            content = {'message': message}
        else:
            content = {'message': 'You don\'t have the right to delete the Blob {0}'.format(blob_object.id)}
            status_code = status.HTTP_401_UNAUTHORIZED

        return Response(content, status=status_code)
    except exceptions.DoesNotExist as e:
        content = {'message': 'No blob found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def delete_list(request):
    """ Delete a list of blobs.

    POST http://<server_ip>:<server_port>/<rest_main>/blob/list/delete

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"blob_ids": ["id1", "id2"]}

    """
    try:
        messages = []
        blob_objects = []
        serializer = serializers.DeleteBlobsSerializer(data=request.data)
        if serializer.is_valid():
            blob_ids = serializer.data.get('blob_ids')
            # Check if all blob exist
            for blob_id in blob_ids:
                blob_object = blob_api.get_by_id(blob_id)
                # Check rights
                if str(request.user.id) == blob_object.user_id or request.user.is_staff:
                    blob_objects.append(blob_object)
                else:
                    content = {'message': 'You don\'t have the right to delete the Blob {0}'.format(blob_object.id)}
                    return Response(content, status=status.HTTP_401_UNAUTHORIZED)

            # Delete blobs
            for blob_object in blob_objects:
                message, status_code = _delete_blob(blob_object)
                messages.append({'message': message, 'status_code': status_code})

            content = {'message': messages}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'message': 'Expected parameters not provided.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist as api_exception:
        content = {'message': 'All Blob have not been found: {0}.'.format(api_exception.message)}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except Exception as api_exception:
        content = {'message': api_exception.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _delete_blob(blob_object):
    """ Delete a blob.

    Args:
        blob_object: Blob to delete.

    Returns:
        message: Message content.
        status_code: status code

    """
    try:
        blob_api.delete(blob_object)
        content = 'Blob {0} deleted with success.'.format(str(blob_object.id))
        status_code = status.HTTP_200_OK
    except Exception as api_exception:
        content = 'An error occurred when attempting to delete the blob (id {0}): {1}'.format(str(blob_object.id),
                                                                                              api_exception.message)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return content, status_code


@api_view(['GET'])
def list_all(request):
    """ List all blobs.

    GET http://<server_ip>:<server_port>/<rest_main>/blob/list

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    """
    try:
        if request.user.is_staff:
            blob_list = blob_api.get_all()
        else:
            blob_list = blob_api.get_all_by_user_id(user_id=request.user.id)

        blobs_info = _get_list_blob_info(blob_list, request)
        return Response(blobs_info, status=status.HTTP_200_OK)
    except:
        content = {'message': 'Something went wrong while listing the BLOB.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_list_blob_info(list_blob, request):
    """ Get list blob info.
    Args:
        list_blob:
        request:

    Returns:

    """
    files = []
    for blob in list_blob:
        item = {'name': blob.filename,
                'id': str(blob.id),
                'uploadDate': str(blob.id.generation_time),
                'handle': get_blob_download_uri(blob, request)
                }
        if request.user.is_staff:
            user = user_api.get_user_by_id(blob.user_id)
            item.update({'user': user.username})
        files.append(item)

    return files
