""" Serializers for Django Group
"""
from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer"""

    class Meta(object):
        """Meta"""

        model = Group
        fields = ("id", "name")
