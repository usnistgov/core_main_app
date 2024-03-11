""" Templatetags to get JSON format and display according to parsing directives
"""

from django import template
import json

from core_main_app.utils.json_utils import load_json_string

register = template.Library()


@register.filter(name="format_json")
def render_json_as_html_detail(content):
    """Render an JSON as HTML detail.
    Args:
        content:

    Returns:
        HTML

    """
    json_object = load_json_string(content)
    return json.dumps(json_object, indent=8)
