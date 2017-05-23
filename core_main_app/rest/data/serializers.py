"""Serializers used throughout the data Rest API
"""
from core_main_app.settings import DATA_AUTO_PUBLISH
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.serializers import Serializer, CharField, BooleanField, DateTimeField
from core_main_app.components.data.models import Data


class DataSerializer(DocumentSerializer):
    """ Data serializer
    """
    class Meta:
        """ Meta
        """
        model = Data
        fields = ["id",
                  "template",
                  "user_id",
                  "title",
                  "xml_content",
                  "is_published",
                  "publication_date",
                  "last_modification_date"]


class CreateDataSerializer(Serializer):
    """ Data serializer (creation)
    """
    template = CharField()
    title = CharField()
    xml_content = CharField()


class UpdateDataSerializer(Serializer):
    """ Data serializer (update)
    """
    id = CharField()
    title = CharField(required=False, default=None)
    xml_content = CharField(required=False, default=None)
