""" Web page model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.commons.enums import WEB_PAGE_TYPES


class WebPage(models.Model):
    """Represents a WebPage"""

    type = models.IntegerField()
    content = models.TextField()

    @staticmethod
    def get_by_type(page_type):
        """Get a WebPage given its type

        Parameters:
            page_type (str): page type

        Returns:
            Web Page corresponding to the given type
        """
        try:
            return WebPage.objects.get(type=WEB_PAGE_TYPES[page_type])
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def delete_by_type(page_type_key):
        """Delete all WebPage with the given type key

        Args:
            page_type_key (int): page type key

        Returns:

        """
        return WebPage.objects.filter(type=page_type_key).delete()
