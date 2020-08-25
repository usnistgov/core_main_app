""" Serializers for Django User
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta(object):
        """Meta"""

        model = User
        fields = ("id", "username")
