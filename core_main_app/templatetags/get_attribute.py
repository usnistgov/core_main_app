""" Get attribute
"""

from django import template

register = template.Library()


@register.filter(name="get_attribute")
def get_attribute(value, arg):
    """get attribute

    https://stackoverflow.com/q/844746

    Args:
        value:
        arg:

    Returns:

    """

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    if isinstance(value, dict) and arg in value:
        return value[arg]
    if arg.isdigit() and len(value) > int(arg):
        return value[int(arg)]
    return ""
