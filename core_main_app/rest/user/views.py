""" REST views for the User API
"""

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.components.user import api as user_api
from core_main_app.rest.user.serializers import UserSerializer


class UserDetail(APIView):
    """Retrieve  User"""

    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        """Get user from db

        Args:

            request: HTTP request
            pk: UserId

        Returns:

            User
        """
        try:

            user_object = user_api.get_user_by_id(pk)

            # Serialize object
            serializer = UserSerializer(user_object)

            # Return response
            return Response(serializer.data)
        except Http404:
            content = {"message": "User not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(APIView):
    """List all Users"""

    permission_classes = (IsAdminUser,)

    def get(self, request):
        """Get all users from db

        Args:

            request: HTTP request

        Returns:

            all users
        """
        try:

            user_object_list = user_api.get_all_users()

            # Serialize object
            serializer = UserSerializer(user_object_list, many=True)

            # Return response
            return Response(serializer.data)

        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
