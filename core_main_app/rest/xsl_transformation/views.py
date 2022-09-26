""" REST Views for XSLT Transformation
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation import api as xsl_api
from core_main_app.rest.xsl_transformation.serializers import (
    XslTransformationSerializer,
    TransformSerializer,
)


class XslTransformationList(APIView):
    """List, create XSL document"""

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get all XSL document

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of XSL document
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            xsl_object_list = xsl_api.get_all()
            # Serialize object
            return_value = XslTransformationSerializer(
                xsl_object_list, many=True
            )
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Save an XSL document

        Parameters:

            {
                "name": "instance_name",
                "filename": "url",
                "content": "<content />",
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created XSL document
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            xsl_serializer = XslTransformationSerializer(data=request.data)
            # Validate xsl
            xsl_serializer.is_valid(raise_exception=True)
            # save or update the object
            xsl_serializer.save()
            return Response(
                xsl_serializer.data, status=status.HTTP_201_CREATED
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class XslTransformationDetail(APIView):
    """ " Get, delete, patch an XSL document"""

    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        """Get XSL document from db

        Args:

            pk: ObjectId

        Returns:

            XSL document
        """
        try:
            return xsl_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Retrieve XSLT

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: XSL document
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Serialize object
            return_value = XslTransformationSerializer(xsl_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {"message": "Xsl not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """Delete an xsl document

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Remove the instance
            xsl_api.delete(xsl_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {"message": "Xsl not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """Update xsl

        Parameters:

            {
                "name": "instance_name",
                "filename": "url",
                "content": "<content />",
            }

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Updated XSL document
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Build serializer
            xsl_serializer = XslTransformationSerializer(
                instance=xsl_object, data=request.data, partial=True
            )
            # Validate xsl
            xsl_serializer.is_valid(raise_exception=True)
            # Save xsl
            xsl_serializer.save()
            return Response(xsl_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {"message": "Xsl not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class XslTransformationTransform(APIView):
    """Transform XML using a specific Xslt"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Transform XML using a specific Xslt

        Parameters:

            {
                "xml_content": "<xml />",
                "xslt_name": "name"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: transformed xml content
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = TransformSerializer(data=request.data)
            # Validate data
            serializer.is_valid(raise_exception=True)
            # transform
            return_value = xsl_api.xsl_transform(**serializer.validated_data)
            return Response(return_value, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
