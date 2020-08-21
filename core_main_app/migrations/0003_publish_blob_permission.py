# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core_main_app", "0002_site_update"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="Main",
            options={
                "verbose_name": "core_main_app",
                "default_permissions": (),
                "permissions": (("publish_blob", "Can publish blob"),),
            },
        ),
    ]
