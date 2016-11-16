"""
Template models
"""

from django_mongoengine import fields, Document


class Template(Document):
    """Represents an XML schema template that defines the structure of data for curation"""
    filename = fields.StringField()
    content = fields.StringField()
    hash = fields.StringField()
    dependencies = fields.ListField(fields.ReferenceField("self"), default=[], blank=True)

    @staticmethod
    def get_all():
        """Returns all templates

        Returns:

        """
        return Template.objects.all()

    @staticmethod
    def get_by_id(template_id):
        """Returns a template by its id

        Args:
            template_id:

        Returns:

        """
        return Template.objects().get(pk=str(template_id))
