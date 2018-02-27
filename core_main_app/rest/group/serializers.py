""" Serializers for Django Group
"""
from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """ Group serializer
    """
    class Meta:
        """ Meta
        """
        model = Group
        fields = ('id', 'name')