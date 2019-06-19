import io

from django import template
from django.contrib.staticfiles import finders
from django.template.base import Template

register = template.Library()


@register.simple_tag(takes_context=True)
def include_static(context, path, encoding="utf-8"):
    file_path = finders.find(path)
    with io.open(file_path, "r", encoding=encoding) as f:
        string = f.read()

    t = Template(string)

    return t.render(context)
