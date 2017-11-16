"""Serializers used throughout the data Rest API
"""
from rest_framework.serializers import Serializer, CharField
from rest_framework_mongoengine.serializers import DocumentSerializer

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
                  "last_modification_date"]


# FIXME: Should use in the future an serializer with dynamic fields (init depth with parameter for example)
class DataWithTemplateInfoSerializer(DocumentSerializer):
    """ Data Full serializer
    """
    class Meta:
        """ Meta
        """
        model = Data
        depth = 2
        fields = ["id",
                  "template",
                  "user_id",
                  "title",
                  "xml_content",
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
