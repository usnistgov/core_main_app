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
    user = fields.StringField(blank=True)
    hash = fields.StringField()
    _display_name = fields.StringField(blank=True)
    dependencies = fields.ListField(
        fields.ReferenceField("self"), default=[], blank=True
    )

    meta = {"allow_inheritance": True}

    @staticmethod
    def get_all(is_cls, users=None):
        """Return all templates.

        Args:
            is_cls (bool): True if filtering by templates only.
            users (list|None): List of users having access to the template.

        Returns:
            list<Template> - List of template following the query parameters.
        """
        template_query_kwargs = dict()

        if is_cls:  # will return all Template object only
            template_query_kwargs["_cls"] = Template.__name__

        if users is not None:  # select specific user if it is defined
            template_query_kwargs["user__in"] = users

        return Template.objects(**template_query_kwargs).all()

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
    def get_all_by_hash(template_hash, users):
        """Return all template having the given hash.

        Args:
            template_hash: Template hash.
            users:

        Returns:
            List of Template instance.

        """
        if users is not None:
            return Template.objects(hash=template_hash, user__in=users).all()
        return Template.objects(hash=template_hash).all()

    @staticmethod
    def get_all_by_hash_list(template_hash_list, users):
        """Return all template having the given hash list.

        Args:
            template_hash_list: Template hash list.
            users:

        Returns:
            List of Template instance.

        """
        if users is not None:
            return Template.objects(hash__in=template_hash_list, user__in=users).all()
        return Template.objects(hash__in=template_hash_list).all()

    @staticmethod
    def get_all_by_id_list(template_id_list, users=None):
        """Return all template with id in list.

        Args:
            template_id_list:
            users:

        Returns:

        """
        if users is not None:
            return Template.objects(pk__in=template_id_list, user__in=users).all()
        return Template.objects(pk__in=template_id_list).all()

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
