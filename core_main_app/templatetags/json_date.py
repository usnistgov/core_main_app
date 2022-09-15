""" Templatetags to get JSON date format and display according to parsing directives
"""
import logging

import dateutil.parser
from django import template
from django.template.defaultfilters import stringfilter
from django.utils import formats

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter(name="json_date")
@stringfilter
def json_date(value, directive):
    """get JSON date string input and return a formatted date string
    according to the parsing directive

    Args:
        value: input JSON date string
        directive: standard django date format directive

    See: https://docs.djangoproject.com/fr/3.0/ref/templates/builtins/#date
    Returns: formatted string
    """
    formatted_date = value
    try:
        # parse the JSON date
        input_datetime = dateutil.parser.parse(formatted_date)
        # format the date thanks to the directive for UI display
        formatted_date = formats.date_format(input_datetime, directive)
        return formatted_date
    except Exception as exception:
        logger.error(str(exception))
        return formatted_date
