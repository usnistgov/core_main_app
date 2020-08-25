""" Serializers used throughout the data Rest API for the admin user
"""

from core_main_app.components.data.models import Data
from core_main_app.rest.data.serializers import DataSerializer, XMLContentField
from core_main_app.components.data import api as data_api


class AdminDataSerializer(DataSerializer):
    """Admin Data serializer"""

    xml_content = XMLContentField()

    class Meta(object):
        """Meta"""

        model = Data
        fields = [
            "id",
            "template",
            "workspace",
            "user_id",
            "title",
            "xml_content",
            "last_modification_date",
        ]
        read_only_fields = ("id",)

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
            user_id=validated_data["user_id"]
            if "user_id" in validated_data
            else str(validated_data["user"].id),
        )
        if "last_modification_date" in validated_data:
            instance.last_modification_date = validated_data["last_modification_date"]
        # Set xml content
        instance.xml_content = validated_data["xml_content"]
        # Save the data
        data_api.admin_insert(instance, validated_data["user"])
        # Encode the response body
        instance.xml_content = validated_data["xml_content"].encode("utf-8")

        return instance
