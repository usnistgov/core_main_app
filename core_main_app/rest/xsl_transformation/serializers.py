"""Serializers for Xsl transformation
"""
from rest_framework.serializers import CharField, ModelSerializer

from core_main_app.commons.serializers import BasicSerializer
from core_main_app.components.xsl_transformation import api as xsl_api
from core_main_app.components.xsl_transformation.models import XslTransformation


class XslTransformationSerializer(ModelSerializer):
    """
    XslTransformation serializer
    """

    content = CharField(required=True)

    class Meta:
        model = XslTransformation
        fields = ["name", "filename", "checksum", "content"]
        read_only_fields = ["checksum"]

    def create(self, validated_data):
        return xsl_api.upsert(XslTransformation(**validated_data))

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.content = validated_data.get("content", instance.content)
        instance.filename = validated_data.get("filename", instance.filename)
        return xsl_api.upsert(instance)


class TransformSerializer(BasicSerializer):
    xml_content = CharField(required=True)
    xslt_name = CharField(required=True)
