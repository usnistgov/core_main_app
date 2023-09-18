""" Templatetags to get JSON format and display according to parsing directives
"""

from django import template
import json

register = template.Library()


@register.filter(name="format_json")
def render_json_as_html_detail(content):
    """Render an JSON as HTML detail.
    Args:
        content:

    Returns:
        HTML

    """
    json_object = json.loads(content)
    return json.dumps(json_object, indent=8)
