""" Serializers for Django User
"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        """Meta"""

        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """create

        Args:
            validated_data

        Returns:
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """update

        Args:
            instance:
            validated_data:

        Returns:
        """
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)

        password = validated_data.get("password", None)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
