""" Templatetags for core_website_app
"""
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="stripjs")
@stringfilter
def stripjs(value):
    """Removes the javascript tags susceptible to be executed on the client side

    Args:
        value:

    Returns:

    """
    stripped = re.sub(
        r"<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)",
        "",
        force_str(value),
        flags=re.S,
    )
    return mark_safe(stripped)
