"""Serializers used throughout the Rest API
"""
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from core_main_app.components.template.api import init_template_with_dependencies
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.rest.template.serializers import TemplateSerializer
from core_main_app.rest.template_version_manager.utils import load_dependencies


class TemplateVersionManagerSerializer(ModelSerializer):
    """
    Template Version Manager serializer
    """

    versions = ReadOnlyField()
    current = ReadOnlyField()
    disabled_versions = ReadOnlyField()

    class Meta:
        """Meta"""

        model = TemplateVersionManager
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "versions",
            "current",
            "is_disabled",
            "disabled_versions",
        ]

    def create(self, validated_data):
        """Create.

        Args:
            validated_data:

        Returns:

        """
        return TemplateVersionManager(**validated_data)


class CreateTemplateSerializer(TemplateSerializer):
    """
    Template Version Manager serializer
    """

    def create(self, validated_data):
        """
        Create and return a new `Template` instance, given the validated data.
        """
        template_object = Template(
            filename=validated_data["filename"],
            content=validated_data["content"],
            user=validated_data["user"],
        )
        template_version_manager_object = validated_data["template_version_manager"]

        # load dependencies
        dependencies_dict = load_dependencies(validated_data)

        # Update the content of the template with dependencies
        init_template_with_dependencies(
            template_object, dependencies_dict, request=self.context["request"]
        )

        # Create the template and its template version manager
        template_version_manager_api.insert(
            template_version_manager_object,
            template_object,
            request=self.context["request"],
        )

        return template_object

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "Template Version Manager should only be updated using specialized APIs."
        )
