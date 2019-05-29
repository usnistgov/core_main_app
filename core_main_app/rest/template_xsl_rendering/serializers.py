""" Serializers used throughout the TemplateXslRendering Rest API
"""
from builtins import object
from rest_framework_mongoengine.fields import ReferenceField
from rest_framework_mongoengine.serializers import DocumentSerializer

from core_main_app.components.template.models import Template
from core_main_app.components.template_xsl_rendering import api as template_xsl_rendering_api
from core_main_app.components.template_xsl_rendering.models import TemplateXslRendering


class TemplateXslRenderingSerializer(DocumentSerializer):
    """ TemplateXslRendering Serializer
    """
    template = ReferenceField(model=Template)

    class Meta(object):
        """ Meta class
        """
        model = TemplateXslRendering
        fields = "__all__"

    def update(self, instance, validated_data):
        """ Update and return an existing `TemplateXslRendering` instance, given the validated data.
        """
        template_id = validated_data.get("template", None)
        list_xslt = validated_data.get("list_xslt", None)
        detail_xslt = validated_data.get("detail_xslt", None)

        return template_xsl_rendering_api.upsert(
            template_id, list_xslt, detail_xslt, template_xsl_rendering_id=instance.id
        )
