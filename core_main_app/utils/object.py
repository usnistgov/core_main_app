""" Utilities for operating on objects/dictionaries.
"""

import logging

logger = logging.getLogger(__name__)


def parse_property(obj, property_name, cast_fn=None):
    """Return the property from an object/dictionary

    Args:
        obj: object|dict - Object or dictionary containing the property.
        property_name: str - Property name to look for.
        cast_fn: A function to cast the property.

    Returns:
        The property value obtained from the object.

    Raises:
        AttributeError: when `property_name` is not present in the object.

    """
    if isinstance(obj, dict) and property_name in obj:
        property_value = obj[property_name]
    elif hasattr(obj, property_name):
        property_value = getattr(obj, property_name)
    else:
        error_message = f"Object {str(obj)} has no property '{property_name}'"
        logger.error(error_message)
        raise AttributeError(error_message)

    if cast_fn:
        try:  # Try casting the result using the casting function
            property_value = cast_fn(property_value)
        except Exception as exc:  # noqa, pylint: disable=broad-except
            logger.warning(
                "Cannot cast %s using %s function: %s",
                str(property_value),
                str(cast_fn),
                str(exc),
            )

    return property_value
