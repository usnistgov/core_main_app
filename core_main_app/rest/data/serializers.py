"""Serializers used throughout the data Rest API
"""

from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

import core_main_app.components.data.api as data_api
from core_main_app.components.data.models import Data


class XMLContentField(serializers.Field):
    """
    XML content is decoded when retrieved - not supported by CharField
    """
    def to_representation(self, obj):
        try:
            return obj.decode('utf-8')
        except AttributeError:
            return obj

    def to_internal_value(self, data):
        return data


class DataSerializer(DocumentSerializer):
    """ Data serializer
    """
    xml_content = XMLContentField()

    class Meta(object):
        """ Meta
        """
        model = Data
        fields = ["id",
                  "template",
                  "workspace",
                  "user_id",
                  "title",
                  "xml_content",
                  "last_modification_date"]
        read_only_fields = ('id', 'user_id', 'last_modification_date', )

    def create(self, validated_data):
        """
        Create and return a new `Data` instance, given the validated data.
        """
        # Create data
        instance = Data(
            template=validated_data['template'],
            workspace=validated_data['workspace'] if 'workspace' in validated_data else None,
            title=validated_data['title'],
            user_id=str(validated_data['user'].id),
        )
        # Set xml content
        instance.xml_content = validated_data['xml_content']
        # Save the data
        data_api.upsert(instance, validated_data['user'])
        # Encode the response body
        instance.xml_content = validated_data['xml_content'].encode('utf-8')

        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing `Data` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.xml_content = validated_data.get('xml_content', instance.xml_content)
        return data_api.upsert(instance, validated_data['user'])


# FIXME: Should use in the future an serializer with dynamic fields (init depth with parameter for example)
class DataWithTemplateInfoSerializer(DocumentSerializer):
    """ Data Full serializer
    """
    class Meta(object):
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

