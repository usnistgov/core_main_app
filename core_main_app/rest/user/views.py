""" REST views for the User API
"""

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from core_main_app.rest.user.serializers import UserSerializer


@extend_schema(
    tags=["User"],
    description="User List Create View",
)
class UserListCreateView(ListCreateAPIView):
    """User List Create View"""

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=["User"],
    description="User Retrieve Update View",
)
class UserRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    """User Retrieve Update View"""

    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
