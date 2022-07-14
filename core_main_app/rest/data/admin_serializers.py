""" Serializers used throughout the data Rest API for the admin user
"""

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.rest.data.serializers import DataSerializer, XMLContentField


class AdminDataSerializer(DataSerializer):
    """Admin Data serializer"""

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
            "creation_date",
            "last_modification_date",
            "last_change_date",
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
            else str(self.context["request"].user.id),
        )
        # Set XML content
        instance.xml_content = validated_data["xml_content"]
        # Set times
        instance.creation_date = validated_data.get("creation_date", None)
        instance.last_modification_date = validated_data.get(
            "last_modification_date", None
        )
        instance.last_change_date = validated_data.get("last_change_date", None)
        # Save the data
        data_api.admin_insert(instance, request=self.context["request"])
        # Encode the response body
        # NOTE: using xml_content property would update the last_modification_date
        instance._xml_content = validated_data["xml_content"].encode("utf-8")

        return instance
