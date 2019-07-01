""" REST views for the template XSL rendering API
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering import api as template_xsl_rendering_api
from core_main_app.rest.template_xsl_rendering.serializers import TemplateXslRenderingSerializer
from core_main_app.access_control.exceptions import AccessControlError


class TemplateXslRenderingList(APIView):
    """ List all template XSL renderings, or create a new one
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """ Get all templates XSL renderings

        Args:
            request: HTTP request

        Returns:
            - code: 200
              content: List of XSL renderings
            - code: 401
              content: Unauthorized
            - code: 500
              content: Internal server error
        """
        try:
            # Retrieve all objects
            template_xsl_rendering_list = template_xsl_rendering_api.get_all()

            # Serialize object
            serializer = TemplateXslRenderingSerializer(template_xsl_rendering_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """ Create a XSL template rendering

        Parameters:
            {
                "template": "template_object_id",
                "list_xslt": "xslt_object_id",
                "detail_xslt": "xslt_object_id"
            }

        Args:
            request: HTTP request

        Returns:
            - code: 201
              content: XSL rendering created
            - code: 400
              content: Validation error / not unique / model error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = TemplateXslRenderingSerializer(data=request.data)

            # Validate data
            serializer.is_valid(True)

            # Save data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ModelError as validation_exception:
            content = {'message': str(validation_exception)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.NotUniqueError as validation_exception:
            content = {'message': str(validation_exception)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as validation_exception:
            content = {'message': validation_exception}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TemplateXslRenderingDetail(APIView):
    """ TemplateXslRendering details view
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """ Get `TemplateXSLRendering` object from db

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            TemplateXSLRendering
        """
        try:
            # Get object
            template_xsl_rendering_object = template_xsl_rendering_api.get_by_id(pk)

            # Serialize object
            template_xsl_rendering_serializer = TemplateXslRenderingSerializer(
                template_xsl_rendering_object
            )

            # Return response
            return Response(template_xsl_rendering_serializer.data)
        except exceptions.DoesNotExist:
            content = {'message': 'XSL rendering object not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """ Edit `TemplateXSLRendering` object from db

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            TemplateXSLRendering
        """
        try:
            # Get object
            template_xsl_rendering_object = template_xsl_rendering_api.get_by_id(pk)

            # Build serializer
            template_xsl_rendering_serializer = TemplateXslRenderingSerializer(
                instance=template_xsl_rendering_object,
                data=request.data
            )

            # Validate data
            template_xsl_rendering_serializer.is_valid(True)
            # Save data
            template_xsl_rendering_serializer.save()

            return Response(template_xsl_rendering_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete a TemplateXSLRendering

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
            template_xsl_rendering_object = template_xsl_rendering_api.get_by_id(pk)

            # delete object
            template_xsl_rendering_api.delete(template_xsl_rendering_object)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = {'message': 'Template XSL rendering not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as ace:
            content = {'message': str(ace)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
