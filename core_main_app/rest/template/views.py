""" REST views for the template API
"""
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.rest.template.serializers import TemplateSerializer
from core_main_app.utils.file import get_file_http_response


class TemplateDetail(APIView):
    """Retrieve a Template."""

    def get_object(self, pk, request):
        """Get Template from db

        Args:

            pk: ObjectId
            request:

        Returns:

            Template
        """
        try:
            return template_api.get(pk, request=request)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Retrieve a Template

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Template
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_object = self.get_object(pk, request=request)

            # Serialize object
            serializer = TemplateSerializer(template_object)

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError:
            content = {"message": "Access Forbidden."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TemplateDownload(APIView):
    """Download a Template"""

    def get_object(self, pk, request):
        """Get Template from db

        Args:

            pk: ObjectId
            request:

        Returns:

            Template
        """
        try:
            return template_api.get(pk, request=request)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Download the XSD file from a Template

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: XSD file
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_object = self.get_object(pk, request=request)

            return get_file_http_response(
                template_object.content, template_object.filename, "text/xsd", "xsd"
            )
        except Http404:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError:
            content = {"message": "Access Forbidden."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
