"""
Version Manager API
"""

from core_main_app.commons import exceptions
from core_main_app.components.version_manager.models import VersionManager


def get(version_manager_id):
    """Gets a version manager by its id

    Args:
        version_manager_id:

    Returns:

    """
    return VersionManager.get_by_id(version_manager_id)


def get_from_version(version):
    """Returns a version manager from a version

    Args:
        version:

    Returns:

    """
    version_managers = VersionManager.get_all()
    for version_manager in version_managers:
        if str(version.id) in version_manager.versions:
            return version_manager
    raise exceptions.ApiError("No version manager could be found for this version.")


def disable(version_manager):
    """Disables an object, then saves it.

    Args:
        version_manager:

    Returns:

    """
    version_manager.disable()
    return upsert(version_manager)


def restore(version_manager):
    """Restores an object, then saves it.

    Args:
        version_manager:

    Returns:

    """
    version_manager.restore()
    return upsert(version_manager)


def restore_version(version):
    """Disables a version of the object, then saves it.

    Args:
        version:

    Returns:

    """
    version_manager = get_from_version(version)
    version_manager.restore_version(version)
    return upsert(version_manager)


def disable_version(version, new_current=None):
    """Disables a version of the object, then saves it.

    Args:
        version:
        new_current:

    Returns:

    """
    version_manager = get_from_version(version)

    # try to delete the current version
    if version_manager.current == str(version.id):
        # no version to be current provided
        if new_current is None:
            raise exceptions.ApiError('Unable to disable the current version.')

        # id doesn't match a version
        if new_current.id not in version_manager.versions:
            raise exceptions.ApiError('The id provided to be the next current version, could not be found.')

        # set the new current version
        version_manager.set_current_version(new_current)

    # disable the version
    version_manager.disable_version(version)
    return upsert(version_manager)


def set_current(version):
    """Sets the current version of the object, then saves it.

    Args:
        version:

    Returns:

    """
    version_manager = get_from_version(version)

    # a disabled version cannot be current
    if str(version.id) in version_manager.get_disabled_versions():
        raise exceptions.ApiError("Unable to set the current version because it is disabled.")

    version_manager.set_current_version(version)
    return upsert(version_manager)


def get_current(version_manager):
    """Gets the current version of the version manager

    Args:
        version_manager:

    Returns:

    """
    return version_manager.current


def upsert(version_manager):
    """Saves or Updates version manager

    Args:
        version_manager:

    Returns:

    """
    return version_manager.save()


def insert_version(version_manager, version):
    """Inserts a version in the version manager, then saves it.

    Args:
        version_manager:
        version:

    Returns:

    """
    version_manager.insert(version)

    # first version inserted, set it as current
    if len(version_manager.versions) == 1:
        version_manager.set_current_version(version)

    return upsert(version_manager)


def get_global_version_managers():
    """Returns all Version Managers with user set to None

    Returns:

    """
    return VersionManager.get_global_version_managers()
