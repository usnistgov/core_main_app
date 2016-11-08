"""
Template models
"""

from django_mongoengine import fields, Document


class Template(Document):
    """Represents an XML schema template that defines the structure of data for curation"""
    filename = fields.StringField()
    content = fields.StringField()
    hash = fields.StringField()
    dependencies = fields.ListField(default=[], blank=True)

    @staticmethod
    def get_all():
        """
        Return all templates
        :return:
        """
        return Template.objects()

    @staticmethod
    def get_by_id(template_id):
        """
        Return a template by its id
        :param template_id:
        :return:
        """
        return Template.objects().get(pk=str(template_id))
