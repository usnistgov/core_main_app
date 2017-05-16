""" REST views for the blob API
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core_main_app.commons import exceptions
import core_main_app.components.blob.api as blob_api
from core_main_app.utils.file import get_file_http_response


@api_view(['GET'])
def download(request):
    """Downloads the blob file

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