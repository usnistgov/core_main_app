""" App model to manage permissions.
"""
from django.db import models

from core_main_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name


class Main(models.Model):
    class Meta:
        verbose_name = 'core_main_app'
        default_permissions = ()
        permissions = (
            (rights.publish_data, get_formatted_name(rights.publish_data)),
        )
