""" Rest views
"""
from importlib import metadata

from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.utils.databases.backend import (
    uses_postgresql_backend,
    uses_sqlite3_backend,
)
from core_main_app.utils.databases.mongo import MONGO_CLIENT


class CoreSettings(APIView):
    """Get Core Settings"""

    permission_classes = (IsAuthenticated,)

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
            # Get version of core main application
            try:
                core_version = metadata.version("core_main_app")
            except metadata.PackageNotFoundError:
                core_version = None

            # Get version of MongoDB server
            mongodb_version = (
                (MONGO_CLIENT.database.client.server_info()["version"])
                if MONGO_CLIENT
                else None
            )

            # Get PSQL version
            if uses_postgresql_backend():
                database_info = (
                    "PostgreSQL",
                    connection.cursor().connection.server_version,
                )
            # Get SQLite version
            elif uses_sqlite3_backend():
                database_info = (
                    "SQLite3",
                    connection.cursor().db.Database.version,
                )
            else:
                database_info = (None, None)

            response_dict = {
                "core_version": core_version,
                "database": {
                    "engine": database_info[0],
                    "version": database_info[1],
                },
                "mongodb": {
                    "data_indexing": settings.MONGODB_INDEXING,
                    "version": mongodb_version,
                },
            }
            return Response(response_dict, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
