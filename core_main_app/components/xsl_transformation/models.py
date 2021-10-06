""" XslTransformation model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


class XslTransformation(models.Model):
    """XslTransformation object"""

    name = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    filename = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
    )
    content = models.TextField(blank=False)

    def __str__(self):
        """String representation of an object.

        Returns:
            String representation

        """
        return self.name

    @staticmethod
    def get_all():
        """Get all XSL Transformations.

        Returns:

        """
        return XslTransformation.objects.all()

    @staticmethod
    def get_by_id_list(list_id):
        """Return the object with the given list id.

        Args:
            list_id:

        Returns:
            Object collection
        """
        return XslTransformation.objects.filter(pk__in=list_id)

    @staticmethod
    def get_by_name(xslt_name):
        """Get XSL Transformation by name.

        Args:
            xslt_name:

        Returns:

        """
        try:
            return XslTransformation.objects.get(name=xslt_name)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_by_id(xslt_id):
        """Get an XSLT document by its id.

        Args:
            xslt_id: Id.

        Returns:
            XslTransformation object.

        """
        try:
            return XslTransformation.objects.get(pk=xslt_id)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def save_object(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            return self.save()
        except IntegrityError as e:
            raise exceptions.NotUniqueError(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.name = self.name.strip()
        self.filename = self.filename.strip()
