""" Template tag to access a dictionary's key
"""
from django import template

register = template.Library()


# TODO: see if we can do it directly in the template
@register.filter(name="get")
def get(d, k):
    """Get the value of the dictionary with the key.
    Args:
        d: dictionary
        k: key

    Returns: the value

    """
    return d.get(k, None)
