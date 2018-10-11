""" Templatetags for core_website_app
"""
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
import re

register = template.Library()


@register.filter(name="stripjs")
@stringfilter
def stripjs(value):
    """ Removes the javascript tags susceptible to be executed on the client side

    Args:
        value:

    Returns:

    """
    stripped = re.sub(r'<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)', '', force_unicode(value), flags=re.S)
    return mark_safe(stripped)
