""" Common Serializers
"""
from rest_framework.serializers import Serializer


class BasicSerializer(Serializer):
    """Represent a serializer with a basic implementation of the abstract methods create and update."""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
