"""Serializers used throughout the data Rest API
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template import api as template_api
from core_main_app.rest.template.serializers import TemplateSerializer
from core_main_app.settings import BACKWARD_COMPATIBILITY_DATA_XML_CONTENT


class ContentField(serializers.Field):
    """
    Content is decoded when retrieved - not supported by CharField
    """

    _error_message = (
        "Either set `content` or `xml_content` (deprecated). "
        "Set `BACKWARD_COMPATIBILITY_DATA_XML_CONTENT` to `True` "
        "in the project settings to continue using `xml_content`."
    )

    default_error_messages = {
        "required": _(f"This field is required. {_error_message}"),
        "null": _(f"This field may not be null. {_error_message}"),
    }

    def to_representation(self, obj):
        try:
            return obj.decode("utf-8")
        except AttributeError:
            return obj

    def to_internal_value(self, data):
        return data


class DataSerializer(ModelSerializer):
    """Data serializer"""

    if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
        xml_content = ContentField()
    else:
        content = ContentField()

    class Meta:
        """Meta"""

        model = Data
        fields = [
            "id",
            "template",
            "workspace",
            "user_id",
            "title",
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

        if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
            fields.append("xml_content")
        else:
            fields.append("content")

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
        template_api.get_by_id(
            instance.template.id, request=self.context["request"]
        )

        # Set content
        if "content" in validated_data:
            instance.content = validated_data["content"]
        elif "xml_content" in validated_data:  # backward compatibility
            instance.xml_content = validated_data["xml_content"]

        # Save the data and retrieve the inserted object
        inserted_data = data_api.upsert(instance, self.context["request"])

        return inserted_data

    def update(self, instance, validated_data):
        """
        Update and return an existing `Data` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        if "content" in validated_data:
            instance.content = validated_data["content"]
        elif "xml_content" in validated_data:  # backward compatibility
            instance.xml_content = validated_data["xml_content"]
        return data_api.upsert(instance, self.context["request"])


class DataWithTemplateInfoSerializer(ModelSerializer):
    """Data Full serializer"""

    template = TemplateSerializer()

    class Meta:
        """Meta"""

        model = Data
        fields = [
            "id",
            "template",
            "user_id",
            "title",
            "creation_date",
            "last_modification_date",
            "last_change_date",
        ]

        if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
            fields.append("xml_content")
        else:
            fields.append("content")
