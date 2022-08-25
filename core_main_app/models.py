""" App model to manage permissions.
"""
from django.db import models

from core_main_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name


class Main(models.Model):
    """Main model containing several information:

    Attributes:
        Meta.verbose_name (:py:class:`str`): Name of the app.
        Meta.permissions (:py:class:`list`): Default set of permissions bundled with the app.
    """

    class Meta:
        """Meta"""

        verbose_name = "core_main_app"
        default_permissions = ()
        permissions = (
            (rights.PUBLISH_DATA, get_formatted_name(rights.PUBLISH_DATA)),
            (rights.PUBLISH_BLOB, get_formatted_name(rights.PUBLISH_BLOB)),
        )
