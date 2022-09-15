""" Rest views for the web page
"""
import logging

from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.web_page import api as web_page_api
from core_main_app.components.web_page.models import WEB_PAGE_TYPES
from core_main_app.rest.web_page.serializers import WebPageSerializer
from core_main_app.utils.decorators import api_staff_member_required

logger = logging.getLogger("core_main_app.rest.web_page.views")


class WebPageList(APIView):
    """Retrieve, create or delete the web page"""

    web_page_type = None

    def get_object(self):
        """Get the web page from db

        Args:

        Returns:

            Web page
        """
        try:
            return web_page_api.get(self.web_page_type)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request):
        """Retrieve the web page

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: web page
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            web_page = self.get_object()

            # Raise if None
            if web_page is None:
                raise Http404

            # Serialize object
            serializer = WebPageSerializer(web_page)

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {"message": "No custom web page has been created"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create or update the custom web page

        Parameters:

            {
                "content": "new_content"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created web page
            - code: 400
              content: Validation error
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            web_page = self.get_object()

            # Build serializer
            if web_page:
                web_page_serializer = WebPageSerializer(
                    instance=web_page, data=request.data, partial=True
                )
            else:
                web_page_serializer = WebPageSerializer(data=request.data, partial=True)

            # Validate web page
            web_page_serializer.is_valid(True)

            # Save web page
            web_page_serializer.save(type=WEB_PAGE_TYPES[self.web_page_type])

            # Return the serialized web page
            return Response(web_page_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def delete(self, request):
        """Delete the custom web page

        Args:

            request: HTTP request

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        try:
            # delete object
            web_page_api.delete_by_type(WEB_PAGE_TYPES[self.web_page_type])

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
