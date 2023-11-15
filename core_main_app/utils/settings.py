""" Utilities for settings
"""
import logging

logger = logging.getLogger(__name__)


def getattr_from_deprecated_var(
    input_settings, deprecated_var_name, supported_var_name, default_value
):
    """Retrieve value from input settings if it exists, otherwise try to assign
    deprecated variable value.

    Args:
        input_settings:
        deprecated_var_name:
        supported_var_name:
        default_value:

    Returns:
    """
    try:  # Try retrieving the deprecated setting value.
        deprecated_var_value = getattr(input_settings, deprecated_var_name)
        deprecated_var_defined = True

        # Show warning if deprecated setting is still in use.
        logger.warning(
            "Settings variable %s is being deprecated. Please use %s in the future.",
            deprecated_var_name,
            supported_var_name,
        )
    except AttributeError:
        # If the deprecated setting is not set, keep a note of it for supported setting
        # assignment.
        deprecated_var_defined = False

    try:  # Try retrieving the supported setting value.
        supported_var_value = getattr(input_settings, supported_var_name)

        # Show a warning if deprecated setting is also defined.
        if deprecated_var_defined:
            logger.warning(
                "A value has been found for supported settings variable %s, "
                "ignoring value for %s.",
                supported_var_name,
                deprecated_var_name,
            )
    except AttributeError:
        # If the supported setting is not set, try to use the deprecated setting, or the
        # default value, whichever is not defined.
        supported_var_value = (
            deprecated_var_value  # noqa
            if deprecated_var_defined
            else default_value
        )

    return supported_var_value
