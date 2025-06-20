""" REST views for the template API
"""

from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions as exceptions
from core_main_app.commons.exceptions import XMLError
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.rest.template.serializers import TemplateSerializer
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.file import (
    get_file_http_response,
    get_template_file_content_type_for_template_format,
    get_template_file_extension_for_template_format,
)
from core_main_app.utils.json_utils import format_content_json
from core_main_app.utils.xml import format_content_xml


@extend_schema(
    tags=["Template"],
    description="List Templates",
)
class TemplateList(APIView):
    """List templates"""

    permission_classes = (IsAuthenticated,)

    def _get_templates(self, request):
        """Retrieve templates
        Args:
            request:
        Returns:
        """
        return template_api.get_all(request=request)

    @extend_schema(
        description="Get templates",
        parameters=[
            OpenApiParameter(
                name="filename",
                description="Filter by filename",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="title",
                description="Filter by title",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="regex",
                description="Enable regular expression matching for filename and title filters (default: False)",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="active_only",
                description="Filter by active templates (current and enabled, default: True)",
                required=False,
                type=bool,
            ),
            OpenApiParameter(
                name="template_format",
                description="Filter by template format (XSD, JSON)",
                required=False,
                type=str,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=TemplateSerializer(many=True),
                description="List of templates",
            ),
            403: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
                description="Authentication error",
            ),
            500: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
                description="Internal server error",
            ),
        },
    )
    def get(self, request):
        """Get templates
        Url Parameters:
            filename: filter by filename
            title: filter by title
            regex: enable regular expression matching for filename and title filters (default: False)
            active_only: filter by active templates (current and enabled, default: True)
            template_format: filter by template format (XSD, JSON)
        Examples:
            - Retrieve all templates: GET /templates/
            - Retrieve templates with filename `example.json` GET /templates?filename=example.json
            - Retrieve templates with title `Example Template` using regex GET /templates?title=Example&regex=true
            - Retrieve active templates in JSON format GET /templates?active_only=true&template_format=JSON
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of templates
            - code: 403
              content: Authentication error
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_list = self._get_templates(request=request)
            # Apply filters
            active_only = self.request.query_params.get("active_only", True)
            if to_bool(active_only):
                template_list = template_list.filter(
                    is_current=True, is_disabled=False
                )
            template_format = self.request.query_params.get(
                "template_format", None
            )
            valid_formats = [
                t_format[0] for t_format in Template.FORMAT_CHOICES
            ]
            if template_format:
                if template_format not in valid_formats:
                    content = {
                        "message": f"Unknown format (available formats: {valid_formats}"
                    }
                    return Response(
                        content, status=status.HTTP_400_BAD_REQUEST
                    )
                format_filter = {"format": template_format}
                template_list = template_list.filter(**format_filter)
            regex = self.request.query_params.get("regex", False)
            title = self.request.query_params.get("title", None)
            if title:
                title_filter = (
                    {"version_manager__title__iregex": title}
                    if to_bool(regex)
                    else {"version_manager__title": title}
                )
                template_list = template_list.filter(**title_filter)
            filename = self.request.query_params.get("filename", None)
            if filename:
                filename_filter = (
                    {"filename__iregex": title}
                    if to_bool(regex)
                    else {"filename": title}
                )
                template_list = template_list.filter(**filename_filter)
            # Serialize object
            serializer = TemplateSerializer(template_list, many=True)
            # Return response
            return Response(serializer.data)
        except AccessControlError:
            content = {"message": "Access Forbidden."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Template"],
    description="Retrieve a Template",
)
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
            return template_api.get_by_id(pk, request=request)
        except exceptions.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve a Template",
        description="Retrieve a Template",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Template ID",
            ),
        ],
        responses={
            200: TemplateSerializer,
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
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
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Template"],
    description="Download a Template",
)
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
            return template_api.get_by_id(pk, request=request)
        except exceptions.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Download the XSD file from a Template",
        description="Download the XSD file from a Template",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Template ID",
            ),
            OpenApiParameter(
                name="pretty_print",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Pretty print the content",
            ),
        ],
        responses=OpenApiResponse(response={"application/octet-stream": {}}),
    )
    def get(self, request, pk):
        """Download the XSD file from a Template
        Args:
            request: HTTP request
            pk: ObjectId
        Examples:
            ../template/[template_id]/download
            ../template/[template_id]/download?pretty_print=false
        Returns:
            - code: 200
              content: XSD file
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_object = self.get_object(pk, request=request)
            # get xml content
            content = template_object.content
            # get format bool
            pretty_print = request.query_params.get("pretty_print", False)
            # format content
            if to_bool(pretty_print):
                # format XML
                if template_object.format == Template.XSD:
                    content = format_content_xml(content)
                # format JSON
                elif template_object.format == Template.JSON:
                    content = format_content_json(content)
                else:
                    content = {"message": "Unsupported format."}
                    return Response(
                        content, status=status.HTTP_400_BAD_REQUEST
                    )
            return get_file_http_response(
                content,
                template_object.filename,
                content_type=get_template_file_content_type_for_template_format(
                    template_object.format
                ),
                extension=get_template_file_extension_for_template_format(
                    template_object.format
                ),
            )
        except Http404:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except XMLError:
            content = {"message": "Content is not well formatted XML."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError:
            content = {"message": "Access Forbidden."}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
