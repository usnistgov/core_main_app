""" Utils to provide regex validation
"""
import re

from django.core.exceptions import ValidationError
from django.core.files.utils import validate_file_name

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


def validate_alphanum(name):
    """Validate alpha-numerical characters

    Args:
        name:

    Returns:

    """
    if re.match(r"^[a-zA-Z][a-zA-Z0-9]+$", name) is None:
        raise ValidationError(
            "Name should only contains alpha-numerical characters."
        )


def validate_filename(filename):
    """Validate filename

    Args:
        filename:

    Returns:

    """
    # Run validate filename from Django
    validate_file_name(filename)
    # Regex check filename has extension
    if re.match(r"^[a-zA-Z0-9-_]+\.[a-z0-9]{2,4}$", filename) is None:
        raise ValidationError("Invalid filename.")
