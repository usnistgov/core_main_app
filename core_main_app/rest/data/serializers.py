"""Serializers used throughout the data Rest API
"""
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import Serializer, CharField, BooleanField, DateTimeField, OrderedDict
from core_main_app.components.data.models import Data


class DataSerializer(DocumentSerializer):
    """ Data serializer
    """
    class Meta:
        """ Meta
        """
        model = Data
        fields = "__all__"


class CreateDataSerializer(Serializer):
    """ Data serializer (creation)
    """
    template = CharField()
    user_id = CharField()
    dict_content = OrderedDict(required=False)
    title = CharField()
    xml_file = CharField()
    is_published = BooleanField(required=False)
    publication_date = DateTimeField(required=False)
    last_modification_date = DateTimeField(required=False)

    def create(self, validated_data):
        """
        Args:
            validated_data:

        Returns:

        """
        return Data(**validated_data)
