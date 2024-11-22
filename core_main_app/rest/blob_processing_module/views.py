""" REST API views for blob processing modules.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.blob_processing_module import (
    api as blob_processing_module_api,
)
from core_main_app.rest.blob_processing_module.serializers import (
    BlobProcessingModuleSerializer,
)


class BlobProcessingModuleView(APIView):
    """CRUD views for blob processing modules."""

    permission_classes = (IsAuthenticated,)

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
            serializer = BlobProcessingModuleSerializer(
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
