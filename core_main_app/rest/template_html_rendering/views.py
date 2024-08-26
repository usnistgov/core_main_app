""" REST views for the template HTML rendering API
"""

from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)

from core_main_app.rest.template_html_rendering.serializers import (
    TemplateHtmlRenderingSerializer,
)


class TemplateHtmlRenderingList(APIView):
    """List all template HTML renderings, or create a new one"""

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get all templates HTML renderings

        Args:
            request: HTTP request

        Returns:
            - code: 200
              content: List of HTML renderings
            - code: 401
              content: Unauthorized
            - code: 500
              content: Internal server error
        """
        try:
            # Retrieve all objects
            template_html_rendering_list = (
                template_html_rendering_api.get_all()
            )

            # Serialize object
            serializer = TemplateHtmlRenderingSerializer(
                template_html_rendering_list, many=True
            )

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Create a HTML template rendering

        Parameters:
            {
                "template": "template_object_id",
                "list_rendering": "list_rendering",
                "detail_rendering": "detail_rendering"
            }

        Args:
            request: HTTP request

        Returns:
            - code: 201
              content: Html rendering created
            - code: 400
              content: Validation error / not unique / model error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = TemplateHtmlRenderingSerializer(data=request.data)

            # Validate data
            serializer.is_valid(raise_exception=True)

            # Save data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (
            ValidationError,
            exceptions.ModelError,
            exceptions.NotUniqueError,
        ) as validation_exception:
            content = {
                "message": str(
                    getattr(
                        validation_exception, "detail", validation_exception
                    )
                )
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TemplateHtmlRenderingDetail(APIView):
    """TemplateHtmlRendering details view"""

    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        """Get `TemplateHtmlRendering` object from db

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            TemplateHtmlRendering
        """
        try:
            # Get object
            template_html_rendering_object = (
                template_html_rendering_api.get_by_id(pk)
            )

            # Serialize object
            template_html_rendering_serializer = (
                TemplateHtmlRenderingSerializer(template_html_rendering_object)
            )

            # Return response
            return Response(template_html_rendering_serializer.data)
        except exceptions.DoesNotExist:
            content = {"message": "Template html rendering not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """Edit `TemplateHtmlRendering` object from db

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            TemplateHtmlRendering
        """
        try:
            # Get object
            template_html_rendering_object = (
                template_html_rendering_api.get_by_id(pk)
            )

            template_html_rendering_serializer = (
                TemplateHtmlRenderingSerializer(
                    instance=template_html_rendering_object,
                    data=request.data,
                    partial=True,
                )
            )

            # Validate data
            template_html_rendering_serializer.is_valid(raise_exception=True)
            # Save data
            template_html_rendering_serializer.save()

            return Response(
                template_html_rendering_serializer.data,
                status=status.HTTP_200_OK,
            )
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Template html rendering not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """Delete a TemplateHtmlRendering

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 204
              content: Deletion successful
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_html_rendering_object = (
                template_html_rendering_api.get_by_id(pk)
            )

            # delete object
            template_html_rendering_api.delete(template_html_rendering_object)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = {"message": "Template html rendering not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BaseDataHtmlRender(APIView, ABC):
    """Base class for Data HTML render"""

    permission_classes = (IsAuthenticated,)

    @abstractmethod
    def get_object(self, pk, request):
        """Abstract method to get data object.

        Args:
            pk:
            request:

        Returns:
             data object.

        """
        raise NotImplementedError("This method is not implemented.")

    def get_rendering_content(self, request, pk):
        """Get the rendering content"""
        try:
            # get data object
            data = self.get_object(pk, request)

            # Retrieve the rendering type from query parameters, default to 'detail'
            rendering_type = request.GET.get("rendering", "detail").lower()

            if rendering_type not in ["list", "detail"]:
                content = {
                    "message": "Rendering type should be list or detail"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            rendering_type_mapping = {
                "list": "list_rendering",
                "detail": "detail_rendering",
            }

            # Get the corresponding field name
            rendering_name = rendering_type_mapping.get(rendering_type)

            # Fetch the template HTML rendering based on the template ID
            template_html_rendering = (
                template_html_rendering_api.get_by_template_id(
                    data.template.id
                )
            )

            # Get the HTML rendering content
            return Response(
                template_html_rendering_api.render_data(
                    template_html_rendering, data, rendering_name
                )
            )

        except exceptions.DoesNotExist:
            content = {"message": "Template HTML rendering or Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {"message": str(ace)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
