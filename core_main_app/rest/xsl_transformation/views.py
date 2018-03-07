""" REST Views for XSLT Transformation
"""
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_main_app.components.xsl_transformation.api as xsl_api
from core_main_app.commons import exceptions
from core_main_app.rest.xsl_transformation.serializers import XslTransformationSerializer, TransformSerializer
from core_main_app.utils.decorators import api_staff_member_required


class XslTransformationList(APIView):
    """
        List, Create XSL document.
    """

    def get(self, request):
        """ Return http response with all xsl document.

            GET /rest/xslt

            Args:
                request:

            Returns:

            """
        try:
            # Get object
            xsl_object_list = xsl_api.get_all()
            # Serialize object
            return_value = XslTransformationSerializer(xsl_object_list, many=True)
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """ Save an xslt.

            POST /rest/xslt
            {
                "name": "instance_name",
                "filename": "url",
                "content": "<content />",
            }

            Args:
                request:

            Returns:

            """
        try:
            # Build serializer
            xsl_serializer = XslTransformationSerializer(data=request.data)
            # Validate xsl
            xsl_serializer.is_valid(True)
            # save or update the object
            xsl_serializer.save()
            return Response(xsl_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class XslTransformationDetail(APIView):
    """" Get, delete, patch an XSL document.
    """

    def get_object(self, pk):
        """ Retrieve an xsl document

        Args:
            pk:

        Returns:

        """
        try:
            return xsl_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Get xslt by its id.

        GET /rest/xslt/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Serialize object
            return_value = XslTransformationSerializer(xsl_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {'message': 'Xsl not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def delete(self, request, pk):
        """ Delete xsl document by its id.

        DELETE /rest/xslt/pk

        Args:
            pk:

        Returns:

        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Remove the instance
            xsl_api.delete(xsl_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {'message': 'Xsl not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def patch(self, request, pk):
        """ Update xsl

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Build serializer
            xsl_serializer = XslTransformationSerializer(instance=xsl_object,
                                                         data=request.data,
                                                         partial=True)
            # Validate xsl
            xsl_serializer.is_valid(True)
            # Save xsl
            xsl_serializer.save()
            return Response(xsl_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {'message': 'Xsl not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class XslTransformationTransform(APIView):
    """
        Transform an Xml using a specific Xslt
    """

    def post(self, request):
        """ Transform

        POST /rest/xslt/transform
        {
            "xml_content": "<xml />",
            "xslt_name": "name"
        }

        Args:
            request:

        Returns:

        """
        try:
            # Build serializer
            serializer = TransformSerializer(data=request.data)
            # Validate data
            serializer.is_valid(True)
            # transform
            return_value = xsl_api.xsl_transform(**serializer.validated_data)
            return Response(return_value, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
