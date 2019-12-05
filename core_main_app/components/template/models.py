"""
Template models
"""
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from django_mongoengine import fields, Document


class Template(Document):
    """Represents an XML schema template that defines the structure of data"""
    filename = fields.StringField(validation=not_empty_or_whitespaces)
    content = fields.StringField()
    hash = fields.StringField()
    _display_name = fields.StringField(blank=True)
    dependencies = fields.ListField(fields.ReferenceField("self"), default=[], blank=True)

    meta = {'allow_inheritance': True}

    @staticmethod
    def get_all(is_cls):
        """Return all templates.

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
        """Return a template by its id.

        Args:
            template_id:

        Returns:

        """
        try:
            return Template.objects().get(pk=str(template_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all_by_hash(template_hash):
        """ Return all template having the given hash.

        Args:
            template_hash: Template hash.

        Returns:
            List of Template instance.

        """
        return Template.objects(hash=template_hash).all()

    @staticmethod
    def get_all_by_hash_list(template_hash_list):
        """ Return all template having the given hash list.

        Args:
            template_hash_list: Template hash list.

        Returns:
            List of Template instance.

        """
        return Template.objects(hash__in=template_hash_list).all()

    @staticmethod
    def get_all_by_id_list(template_id_list):
        """ Return all template with id in list.

        Args:
            template_id_list:

        Returns:

        """
        return Template.objects(pk__in=template_id_list)

    @staticmethod
    def get_all_templates_by_dependencies(dependency_id_list):
        """List all templates having the given dependencies.

        Args:
            dependency_id_list: List of dependency ids.

        Returns:
            List of templates.

        """

        return Template.objects(dependencies__in=dependency_id_list).all()

    @property
    def display_name(self):
        """Return template name to display.

        Returns:

        """
        if self._display_name is not None:
            return self._display_name
        else:
            return self.filename

    @display_name.setter
    def display_name(self, value):
        """Set template name to display.

        Args:
            value:

        Returns:

        """
        self._display_name = value
