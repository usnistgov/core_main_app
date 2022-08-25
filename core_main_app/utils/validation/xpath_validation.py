""" Utils to provide xpath validation
"""
from django.core.exceptions import ValidationError

from core_main_app.commons import exceptions
from core_main_app.utils.xml import validate_xpath


def validate_xpath_list(xpath_list):
    """Validate list of xpaths

    Args:
        xpath_list:

    Returns:

    """
    item_position = 0

    for xpath in xpath_list:
        try:
            validate_xpath(xpath)
            item_position += 1
        except exceptions.XMLError as exception:
            raise ValidationError(
                "XPath syntax error (item #%d): %s" % (item_position, str(exception))
            )
