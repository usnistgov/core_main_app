"""Utils for permissions
"""


def get_formatted_name(permission):
    """Return the formatted name from a permission.

    Args:
        permission:

    Returns:

    """
    return "Can {}".format(permission.replace("_", " "))
