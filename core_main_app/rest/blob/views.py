""" REST views for the blob API
"""
from abc import abstractmethod, ABCMeta

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

import core_main_app.components.blob.api as blob_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.rest.blob.serializers import BlobSerializer, DeleteBlobsSerializer
from core_main_app.utils.file import get_file_http_response


class AbstractBlobList(APIView, metaclass=ABCMeta):

    @abstractmethod
    def _get_blobs(self, request):
        """ Retrieve blobs

        Args:
            request:

        Returns:

        """
        raise NotImplementedError("_get_blobs method is not implemented.")

    def get(self, request):
        """ Get all Blob accessible

        Url Parameters:

            filename: document_filename

        Examples:

            ../blob/
            ../blob?filename=[filename]

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of blob
            - code: 403
              content: Authentication error
            - code: 500
              content: Internal server error
        """
        try:
            blob_list = self._get_blobs(request)

            # Apply filters
            filename = self.request.query_params.get('filename', None)
            if filename is not None:
                blob_list = blob_list.filter(filename=filename)

            # Serialize object
            serializer = BlobSerializer(blob_list, many=True, context={'request': request})

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobListAdmin(AbstractBlobList):
    """ List all Blob
    """
    permission_classes = (IsAdminUser, )

    def _get_blobs(self, request):
        """ Retrieve blobs

        Args:
            request:

        Returns:

        """
        return blob_api.get_all(request.user)


class BlobList(AbstractBlobList):
    """ List all user Blob, or create a new one
    """
    permission_classes = (IsAuthenticated, )

    def _get_blobs(self, request):
        """ Retrieve blobs

        Args:
            request:

        Returns:

        """
        return blob_api.get_all_by_user(user=request.user)

    def post(self, request):
        """ Create Blob

        Parameters:

            {
                "blob": "[file]",
            }

        Code snippet:

            requests.post(url, files={'blob': open(BLOB_PATH, 'rb')}, auth=(USER, PSWD))

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: Created blob
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
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
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDetail(APIView):
    """ Retrieve, update or delete a Blob
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, request, pk):
        """ Get Blob from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Blob
        """
        try:
            return blob_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Retrieve Blob

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Blob
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            blob_object = self.get_object(request, pk)

            # Serialize object
            serializer = BlobSerializer(blob_object, context={'request': request})

            # Return response
            return Response(serializer.data)
        except AccessControlError as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete Blob

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            blob_object = self.get_object(request, pk)

            # delete object
            blob_api.delete(blob_object, request.user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccessControlError as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDownload(APIView):
    """ Download Blob
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, request, pk):
        """ Get Blob from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Blob
        """
        try:
            return blob_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Download the Blob file

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Blob file
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            blob_object = self.get_object(request, pk)

            return get_file_http_response(blob_object.blob, blob_object.filename)
        except AccessControlError as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            content = {'message': 'Blob not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlobDeleteList(APIView):
    """ Delete a list of Blob
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def patch(self, request):
        """ Delete a list of Blob

        Parameters:

            [
                {
                    "id": "blob_id",
                },
                {
                    "id": "blob_id",
                }
            ]

        Args:

            request: HTTP request

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 400
              content: Validation error
            - code: 403
              content: Authentication error
            - code: 500
              content: Internal server error
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
                blob = blob_api.get_by_id(blob_id, request.user)
                # Delete blob
                blob_api.delete(blob, request.user)

            # Return the serialized data
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError as access_control_error:
            content = {'message': str(access_control_error)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
