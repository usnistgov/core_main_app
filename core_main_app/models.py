""" App model to manage permissions.
"""
from django.db import models


class Main(models.Model):
    class Meta:
        verbose_name = 'core_main_app'
        default_permissions = ()
