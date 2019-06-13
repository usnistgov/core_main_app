"""Utils for version manager components
"""


def get_latest_version_name(version_manager):
    """Get name for the latest version of version manager.

    Args:
        version_manager:

    Returns:

    """
    return get_version_name(version_manager.title, str(len(version_manager.versions)))


def get_version_name(title, version_number):
    """Get a version name from a title and a version number.

    Args:
        title:
        version_number:

    Returns:

    """
    return "{0} (Version {1})".format(title, str(version_number))
