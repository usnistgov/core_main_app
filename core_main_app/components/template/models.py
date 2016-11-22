"""
Template models
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


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
        try:
            return Template.objects().get(pk=str(template_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

