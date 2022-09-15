""" Rest views
"""
from importlib_metadata import version, PackageNotFoundError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CoreSettings(APIView):
    """Get Core Settings"""

    def get(self, request):
        """Get Core setting

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: Settings
            - code: 500
              content: Internal server error
        """
        try:
            try:
                core_version = version("core_main_app")
            except PackageNotFoundError:
                core_version = "UNKNOWN"

            response_dict = {
                "core_version": core_version,
            }
            return Response(response_dict, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
