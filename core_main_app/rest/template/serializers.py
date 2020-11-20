"""Serializers used throughout the Rest API
"""
from rest_framework.fields import CharField
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_main_app.components.template.models import Template


class TemplateSerializer(DocumentSerializer):
    """
    Template serializer
    """

    dependencies_dict = CharField(write_only=True, required=False)

    class Meta(object):
        model = Template
        fields = [
            "id",
            "user",
            "filename",
            "content",
            "hash",
            "dependencies",
            "dependencies_dict",
        ]

        read_only_fields = [
            "id",
            "user",
            "hash",
            "_display_name",
        ]
