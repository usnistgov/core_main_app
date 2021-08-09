""" REST views for the User API
"""
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from core_main_app.rest.user.serializers import UserSerializer


class UserListCreateView(ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer
