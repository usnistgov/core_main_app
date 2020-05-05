from __future__ import unicode_literals
from django.db import migrations
from django.contrib.sites.models import Site

from core_main_app.settings import SERVER_URI


def update_site(code, reverse_code):
    site_domain = SERVER_URI

    for i in (("http://", ""), ("https://", "")):
        site_domain = site_domain.replace(*i)

    my_site = Site.objects.get_or_create(id=1)[0]
    my_site.name = site_domain
    my_site.domain = site_domain
    my_site.save()


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0001_initial"),
        ("core_main_app", "0001_main"),
    ]

    operations = [migrations.RunPython(update_site)]
