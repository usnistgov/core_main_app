import io
from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@register.simple_tag
def include_static(path, encoding="utf-8"):
    file_path = finders.find(path)
    with io.open(file_path, "r", encoding=encoding) as f:
        string = f.read()

    return string
