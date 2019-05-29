""" Serializers for Django Group
"""
from builtins import object
from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    """ Group serializer
    """
    class Meta(object):
        """ Meta
        """
        model = Group
        fields = ('id', 'name')