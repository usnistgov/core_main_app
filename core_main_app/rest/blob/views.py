""" REST views for the blob API
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_main_app.components.blob.api as blob_api
from core_main_app.commons import exceptions
from core_main_app.rest.blob.serializers import BlobSerializer, DeleteBlobsSerializer
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.file import get_file_http_response


class BlobList(APIView):
    """ List all user blobs, or create a new one.
    """

    def get(self, request):
        """ Get all user blobs

        /rest/blob/
        /rest/blob/?filename=<filename>

        Query Params:
            filename: filename

        Args:
            request:

        Returns:

        """
        try:
            # FIXME: remove?
            if request.user.is_superuser:
                blob_list = blob_api.get_all()
            else:
                blob_list = blob_api.get_all_by_user_id(user_id=request.user.id)

            # Apply filters
            filename = self.request.query_params.get('filename', None)
            if filename is not None:
                blob_list = blob_list.filter(filename=filename)

            # Serialize object
            serializer = BlobSerializer(blob_list, many=True, context={'request': request})

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """ Create blob

        Data:
            {
            "blob": "<file>",
            "filename": "<filename>"
            }

        Args:
            request:

        Returns:

        """
        try:
            # Build serializer
            serializer = BlobSerializer(data=request.data, context={'request': request})

            # Validate data
            serializer.is_valid(True)

            # Save data
            serializer.save(user=request.user)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDetail(APIView):
    """
    Retrieve, update or delete a blob.
    """

    def get_object(self, pk):
        """ Get blob from db

        Args:
            pk:

        Returns:

        """
        try:
            return blob_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Retrieve blob

        Args:
            pk:

        Returns:

        """
        try:
            # Get object
            blob_object = self.get_object(pk)

            # Serialize object
            serializer = BlobSerializer(blob_object, context={'request': request})

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete a blob

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            blob_object = self.get_object(pk)

            # Check rights
            if request.user.is_superuser is False and str(request.user.id) != blob_object.user_id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # delete object
            blob_api.delete(blob_object)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDownload(APIView):
    """
    Download a blob.
    """

    def get_object(self, pk):
        """ Get blob from db

        Args:
            pk:

        Returns:

        """
        try:
            return blob_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Retrieve blob

        Args:
            pk:

        Returns:

        """
        try:
            # Get object
            blob_object = self.get_object(pk)

            return get_file_http_response(blob_object.blob, blob_object.filename)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDeleteList(APIView):
    """ Delete list of blobs.
    """
    def patch(self, request):
        """ Delete a list of blobs.

        /rest/blobs/delete/

        Data:
        [{"id":"<blob_id>"},{"id":"<blob_id>"}]

        Args:
            request:

        Returns:

        """
        try:
            # Serialize data
            serializer = DeleteBlobsSerializer(data=request.data, many=True, context={'request': request})

            # Validate data
            serializer.is_valid(True)

            # Get list of unique ids
            blob_ids = set([blob['id'] for blob in serializer.validated_data])

            for blob_id in blob_ids:
                # Get blob with its id
                blob = blob_api.get_by_id(blob_id)
                # Delete blob
                blob_api.delete(blob)

            # Return the serialized data
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError as access_control_error:
            content = {'message': access_control_error.message}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
