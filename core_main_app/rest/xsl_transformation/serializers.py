"""Serializers for Xsl transformation
"""
from rest_framework.serializers import CharField
from rest_framework_mongoengine.serializers import DocumentSerializer

import core_main_app.components.xsl_transformation.api as xsl_api
from core_main_app.commons.serializers import BasicSerializer
from core_main_app.components.xsl_transformation.models import XslTransformation


class XslTransformationSerializer(DocumentSerializer):
    """
    XslTransformation serializer
    """

    class Meta(object):
        model = XslTransformation
        fields = "__all__"

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
