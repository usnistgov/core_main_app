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
    _display_name = fields.StringField(blank=True)
    dependencies = fields.ListField(fields.ReferenceField("self"), default=[], blank=True)

    meta = {'allow_inheritance': True}

    @staticmethod
    def get_all(is_cls):
        """Returns all templates

        Returns:

        """
        if is_cls:
            # will return all Template object only
            return Template.objects(_cls=Template.__name__).all()
        else:
            # will return all inherited object
            return Template.object().all()

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

    @staticmethod
    def get_all_by_hash(template_hash):
        """ Returns all template having the given hash.

        Args:
            template_hash: Template hash.

        Returns:
            List of Template instance.

        """
        return Template.objects(hash=template_hash).all()

    @staticmethod
    def get_all_by_id_list(template_id_list):
        """ Returns all template with id in list

        Args:
            template_id_list:

        Returns:

        """
        return Template.objects(pk__in=template_id_list)

    @property
    def display_name(self):
        """Returns template name to display

        Returns:

        """
        if self._display_name is not None:
            return self._display_name
        else:
            return self.filename

    @display_name.setter
    def display_name(self, value):
        """Sets template name to display

        Args:
            value:

        Returns:

        """
        self._display_name = value
