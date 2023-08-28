""" MongoData Serializer
"""
from rest_framework import serializers
from rest_framework.serializers import Serializer

from core_main_app.rest.data.serializers import ContentField
from core_main_app.settings import BACKWARD_COMPATIBILITY_DATA_XML_CONTENT


class MongoDataSerializer(Serializer):
    """Data serializer"""

    id = serializers.IntegerField(read_only=True)
    template = serializers.SerializerMethodField(read_only=True)
    workspace = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)
    last_modification_date = serializers.DateTimeField(read_only=True)
    last_change_date = serializers.DateTimeField(read_only=True)

    if BACKWARD_COMPATIBILITY_DATA_XML_CONTENT:
        xml_content = ContentField(read_only=True)
    else:
        content = ContentField(read_only=True)

    class Meta:
        """Meta"""

        fields = [
            "id",
            "template",
            "workspace",
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

    def get_template(self, obj):
        """Return template id

        Args:
            obj:

        Returns:

        """
        return obj._template_id

    def get_workspace(self, obj):
        """Return workspace id

        Args:
            obj:

        Returns:

        """
        return obj._workspace_id

    def get_user_id(self, obj):
        """Return user id (str)

        Args:
            obj:

        Returns:

        """
        return str(obj.user_id)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
