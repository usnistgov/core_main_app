""" Boolean utils
"""


def to_bool(value):
    """Converts value to python/django bool

    Args:
        value:

    Returns:

    """
    if isinstance(value, bool):
        return value
    if hasattr(value, "upper"):
        if value.upper() == "FALSE":
            return False
        if value.upper() == "TRUE":
            return True

    raise ValueError("Error: a boolean value is expected.")
