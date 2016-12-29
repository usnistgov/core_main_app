"""Serializers used throughout the Rest API
"""
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import Serializer, CharField
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import TemplateVersionManager


class TemplateSerializer(DocumentSerializer):
    """
        Template serializer
    """
    class Meta:
        model = Template
        fields = "__all__"


class TemplateVersionManagerSerializer(DocumentSerializer):
    """
        Template Version Manager serializer
    """
    class Meta:
        model = TemplateVersionManager
        fields = "__all__"


class CreateTemplateSerializer(Serializer):
    """
        Template serializer (creation)
    """
    filename = CharField()
    content = CharField()

    def create(self, validated_data):
        return Template(**validated_data)


class CreateTemplateVersionManagerSerializer(Serializer):
    """
        Template Version Manager serializer (creation)
    """
    title = CharField()

    def create(self, validated_data):
        return TemplateVersionManager(**validated_data)
