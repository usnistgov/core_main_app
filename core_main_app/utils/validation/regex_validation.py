""" Utils to provide regex validation
"""
import re

from mongoengine import ValidationError

from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES


def not_empty_or_whitespaces(value):
    """Check that the value is not an empty string or only white spaces

    Args:
        value:

    Returns:

    """
    pattern = re.compile(NOT_EMPTY_OR_WHITESPACES)
    if not pattern.match(value):
        raise ValidationError("Value can not be empty")
