""" REST views for the User API
"""
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core_main_app.rest.user.serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
    """User List Create View"""

    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    """User Retrieve Update View"""

    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
