""" Web Page serializer
"""
from rest_framework.serializers import ModelSerializer

from core_main_app.components.web_page import api as web_page_api
from core_main_app.components.web_page.models import WebPage


class WebPageSerializer(ModelSerializer):
    """Represents the web page serializer"""

    class Meta:
        """Meta"""

        model = WebPage

        fields = ["id", "type", "content"]

        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create and return a new `WebPage` instance, given the validated data"""
        # Create data
        web_page = WebPage(
            content=validated_data["content"],
            type=validated_data["type"],
        )
        # Save the web page
        return web_page_api.upsert(web_page)

    def update(self, instance, validated_data):
        """Update and return an existing `WebPage` instance, given the validated data"""
        instance.content = validated_data.get("content", instance.content)
        return web_page_api.upsert(instance)
