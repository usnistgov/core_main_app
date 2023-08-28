""" Serializers used throughout the data Rest API for the admin user
"""

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.rest.data.serializers import DataSerializer, ContentField
from core_main_app.settings import BACKWARD_COMPATIBILITY_DATA_XML_CONTENT


class AdminDataSerializer(DataSerializer):
    """Admin Data serializer"""

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
            "creation_date",
            "last_modification_date",
            "last_change_date",
        ]
        read_only_fields = ("id",)

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
            user_id=validated_data["user_id"]
            if "user_id" in validated_data
            else str(self.context["request"].user.id),
        )
        # Set content
        if "content" in validated_data:
            instance.content = validated_data["content"]
        elif "xml_content" in validated_data:  # backward compatibility
            instance.xml_content = validated_data["xml_content"]
        # Set times
        instance.creation_date = validated_data.get("creation_date", None)
        instance.last_modification_date = validated_data.get(
            "last_modification_date", None
        )
        instance.last_change_date = validated_data.get(
            "last_change_date", None
        )
        # Save the data
        data_api.admin_insert(instance, request=self.context["request"])

        return instance
