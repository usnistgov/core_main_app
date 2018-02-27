""" Serializers for Django User
"""
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ User serializer
    """
    class Meta:
        """ Meta
        """
        model = User
        fields = ('id', 'username')
