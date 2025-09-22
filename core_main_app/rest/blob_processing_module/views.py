""" REST API views for blob processing modules.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    PolymorphicProxySerializer,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.blob_processing_module import (
    api as blob_processing_module_api,
)
from core_main_app.rest.blob_processing_module.serializers import (
    BlobProcessingModuleReadSerializer,
    BlobProcessingModuleWriteSerializer,
)


class BlobProcessingModuleDynamicSerializerAPIView(APIView):
    """API View for interacting with Blob Processing Modules.

    This view implements dynamic behavior for both permissions and serialization:
    * Permissions: Read access for authenticated users, write access for admins only.
    * Serialization: Staff users receive a write-capable serializer; others receive a
    read-only version.
    """

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view requires.

        Overrides the default `permission_classes` to enforce stricter access control
        for state-changing methods.

        Returns:
            list: A list containing [IsAdminUser] for non-GET methods (POST, PUT, DELETE),
            otherwise returns the default permissions (parent class implementation).
        """
        if self.request.method != "GET":
            return [IsAdminUser()]
        return super().get_permissions()

    @staticmethod
    def get_serializer(request):
        """Select the appropriate serializer based on the requesting user's privileges.

        Args:
            request: The HTTP request object containing the user instance.

        Returns:
            class: BlobProcessingModuleWriteSerializer if the user is staff,
            otherwise BlobProcessingModuleReadSerializer.
        """
        return (
            BlobProcessingModuleWriteSerializer
            if request.user.is_staff
            else BlobProcessingModuleReadSerializer
        )


@extend_schema(
    tags=["Blob Processing Module"],
    description="CRUD views for blob processing modules",
)
class BlobProcessingModuleListView(
    BlobProcessingModuleDynamicSerializerAPIView
):
    """REST View for listing blob processing modules."""

    @extend_schema(
        summary="Retrieve the list of blob processing modules",
        description="Retrieve the list of blob processing modules",
        responses={
            200: OpenApiResponse(
                PolymorphicProxySerializer(
                    component_name="BlobProcessingModuleResponse",
                    resource_type_field_name=None,
                    serializers=[
                        BlobProcessingModuleWriteSerializer,
                        BlobProcessingModuleReadSerializer,
                    ],
                    many=True,
                ),
                description="List of blob processing modules",
            ),
            403: OpenApiResponse(
                description="User is not authenticated or has no access"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        """Retrieve the list of blob processing modules
        Args:
            request: The HTTP request being sent
        """
        try:
            blob_processing_module_list = blob_processing_module_api.get_all(
                request.user
            )
            # Serialize object
            serializer = self.get_serializer(request)(
                blob_processing_module_list,
                many=True,
                context={"request": request},
            )
            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a new blob processing module",
        description="Create a new blob processing module",
        request=BlobProcessingModuleWriteSerializer,
        responses={
            201: OpenApiResponse(
                BlobProcessingModuleWriteSerializer,
                description="New blob processing module",
            ),
            400: OpenApiResponse(description="The data is not valid"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def post(self, request):
        """Create a new blob processing module
        Args:
            request: The HTTP request being sent
        """
        try:
            # Build serializer
            serializer = self.get_serializer(request)(
                data=request.data, context={"request": request}
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Blob Processing Module"],
    description="CRUD views for blob processing modules",
)
class BlobProcessingModuleManageView(
    BlobProcessingModuleDynamicSerializerAPIView
):
    """REST views for managing blob processing modules."""

    @extend_schema(
        summary="Retrieve a blob processing module",
        description="Retrieve a blob processing module",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,  # noqa
                description="Blob Processing Module ID",
            ),
        ],
        responses={
            200: OpenApiResponse(
                PolymorphicProxySerializer(
                    component_name="BlobProcessingModuleResponse",
                    resource_type_field_name=None,
                    serializers=[
                        BlobProcessingModuleWriteSerializer,
                        BlobProcessingModuleReadSerializer,
                    ],
                ),
                description="Blob processing module",
            ),
            403: OpenApiResponse(
                description="User is not authenticated or has no access"
            ),
            404: OpenApiResponse(
                description="Blob Processing Module was not found"
            ),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, blob_processing_module_id):
        """Retrieve a blob processing module
        Args:
            request: The HTTP request being sent
            blob_processing_module_id: Blob Processing Module ID
        """
        try:
            blob_processing_module_object = (
                blob_processing_module_api.get_by_id(
                    blob_processing_module_id, request.user
                )
            )
            # Serialize object
            serializer = self.get_serializer(request)(
                blob_processing_module_object,
                context={"request": request},
            )
            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except DoesNotExist:
            return Response(
                {"message": "Blob Processing Module not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Modify a Blob Processing Module",
        description="Modify a Blob Processing Module",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,  # noqa
                description="Blob Processing Module ID",
            ),
        ],
        responses={
            200: OpenApiResponse(
                BlobProcessingModuleWriteSerializer(),
                description="Blob Processing Module modified",
            ),
            400: OpenApiResponse(
                description="Invalid Blob Processing Module data"
            ),
            403: OpenApiResponse(description="Access forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def patch(self, request, blob_processing_module_id):
        """Modify an existing blob processing module
        Args:
            request: The HTTP request being sent
            blob_processing_module_id: Blob Processing Module ID
        """
        try:
            # Get object
            blob_processing_module_object = (
                blob_processing_module_api.get_by_id(
                    blob_processing_module_id, request.user
                )
            )
            # Build serializer
            serializer = BlobProcessingModuleWriteSerializer(
                instance=blob_processing_module_object,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            return Response(
                {"message": validation_exception.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DoesNotExist:
            return Response(
                {"message": "Data not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except AccessControlError as exception:
            return Response(
                {"message": str(exception)}, status=status.HTTP_403_FORBIDDEN
            )
        except Exception as api_exception:
            return Response(
                {"message": str(api_exception)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Delete Blob Processing Module",
        description="Delete Blob Processing Module",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,  # noqa
                description="Blob Processing Module ID",
            ),
        ],
        responses={
            204: OpenApiResponse(description="Blob Processing Module deleted"),
            403: OpenApiResponse(description="Access forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def delete(self, request, blob_processing_module_id):
        """Delete Blob Processing Module
        Args:
            request: HTTP request
            blob_processing_module_id: Blob Processing Module ID
        """
        try:
            # Find and delete object
            blob_processing_module_api.delete(
                blob_processing_module_id, request.user
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccessControlError as exception:
            return Response(
                {"message": str(exception)}, status=status.HTTP_403_FORBIDDEN
            )
        except DoesNotExist:
            return Response(
                {"message": "Blob Processing Module not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as api_exception:
            return Response(
                {"message": str(api_exception)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
