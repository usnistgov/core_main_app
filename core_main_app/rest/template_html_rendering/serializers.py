""" Serializers used throughout the TemplateHtmlRendering Rest API
"""

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)
from core_main_app.components.template_html_rendering.models import (
    TemplateHtmlRendering,
)


class TemplateHtmlRenderingSerializer(ModelSerializer):
    """TemplateHtmlRenderingSerializer"""

    class Meta:
        """Meta class"""

        model = TemplateHtmlRendering
        fields = "__all__"

    def create(self, validated_data):
        """create

        Args:
            validated_data

        Returns:
        """
        return template_html_rendering_api.upsert(
            TemplateHtmlRendering(**validated_data)
        )

    def update(self, instance, validated_data):
        """Update and return an existing `TemplateHtmlRendering` instance, given the validated data."""
        if "template" in validated_data:
            raise ValidationError("Template can not be updated")
        instance.list_rendering = validated_data.get(
            "list_rendering", instance.list_rendering
        )
        instance.detail_rendering = validated_data.get(
            "detail_rendering", instance.detail_rendering
        )

        return template_html_rendering_api.upsert(instance)
