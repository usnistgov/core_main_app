""" REST views for the User API
"""
import json

from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.components.user import api as user_api
from core_main_app.rest.user.serializers import UserSerializer
from core_main_app.utils.decorators import api_staff_member_required


class UserDetail(APIView):
    """ Retrieve  User
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    @method_decorator(api_staff_member_required())
    def get(self, request, pk):
        """ Get user from db

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
            content = {'message': 'User not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)