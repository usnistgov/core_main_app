"""Serializers used throughout the data Rest API
"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template import api as template_api


class XMLContentField(serializers.Field):
    """
    XML content is decoded when retrieved - not supported by CharField
    """

    def to_representation(self, obj):
        try:
            return obj.decode("utf-8")
        except AttributeError:
            return obj

    def to_internal_value(self, data):
        return data


class DataSerializer(ModelSerializer):
    """Data serializer"""

    xml_content = XMLContentField()

    class Meta:
        """Meta"""

        model = Data
        fields = [
            "id",
            "template",
            "workspace",
            "user_id",
            "title",
            "xml_content",
            "checksum",
            "creation_date",
            "last_modification_date",
            "last_change_date",
        ]
        read_only_fields = (
            "id",
            "user_id",
            "checksum",
            "creation_date",
            "last_modification_date",
            "last_change_date",
        )

    def create(self, validated_data):
        """
        Create and return a new `Data` instance, given the validated data.
        """
        # Create data
        instance = Data(
            template=validated_data["template"],
            workspace=validated_data["workspace"]
            if "workspace" in validated_data
            else None,
            title=validated_data["title"],
            user_id=str(self.context["request"].user.id),
        )
        # Get template
        template_api.get_by_id(instance.template.id, request=self.context["request"])

        # Set xml content
        instance.xml_content = validated_data["xml_content"]

        # Save the data and retrieve the inserted object
        inserted_data = data_api.upsert(instance, self.context["request"])

        # Encode the response body
        inserted_data.xml_content = inserted_data.xml_content.encode("utf-8")

        return inserted_data

    def update(self, instance, validated_data):
        """
        Update and return an existing `Data` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.xml_content = validated_data.get("xml_content", instance.xml_content)
        return data_api.upsert(instance, self.context["request"])


# FIXME: Should use in the future an serializer with dynamic fields (init depth with parameter for example)
class DataWithTemplateInfoSerializer(ModelSerializer):
    """Data Full serializer"""

    class Meta:
        """Meta"""

        model = Data
        depth = 2
        fields = [
            "id",
            "template",
            "user_id",
            "title",
            "xml_content",
            "creation_date",
            "last_modification_date",
            "last_change_date",
        ]
