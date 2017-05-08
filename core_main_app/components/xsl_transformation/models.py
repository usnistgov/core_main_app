""" XslTransformation model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class XslTransformation(Document):
    """ XslTransformation object
    """
    name = fields.StringField(blank=False, unique=True)
    filename = fields.StringField(blank=False)
    content = fields.StringField(blank=False)

    meta = {'allow_inheritance': True}

    def __str__(self):
        """ String representation of an object.

        Returns:
            String representation

        """
        return self.name

    @staticmethod
    def get_all():
        """

        Returns:

        """
        return XslTransformation.objects.all()

    @staticmethod
    def get_by_name(xslt_name):
        """

        Args:
            xslt_name:

        Returns:

        """
        try:
            return XslTransformation.objects.get(name=xslt_name)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as e:
            raise exceptions.ModelError(e.message)

    @staticmethod
    def get_by_id(xslt_id):
        """ Get an XSLT document by its id.

        Args:
            xslt_id: Id.

        Returns:
            XslTransformation object.

        """
        try:
            return XslTransformation.objects.get(pk=str(xslt_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)
