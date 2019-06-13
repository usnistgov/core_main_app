"""
Version Manager API
"""

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.version_manager.models import VersionManager


def get(version_manager_id):
    """Get a version manager by its id.

    Args:
        version_manager_id:

    Returns:

    """
    return VersionManager.get_by_id(version_manager_id)


def get_by_id_list(list_id):
    """Get a version managers with the given id list.

    Args:
        list_id:

    Returns:

    """
    return VersionManager.get_by_id_list(list_id)


def get_from_version(version):
    """Return a version manager from a version.

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
    """Disable an object, then saves it.

    Args:
        version_manager:

    Returns:

    """
    version_manager.disable()
    return upsert(version_manager)


def restore(version_manager):
    """Restore an object, then saves it.

    Args:
        version_manager:

    Returns:

    """
    version_manager.restore()
    return upsert(version_manager)


def restore_version(version):
    """Disable a version of the object, then saves it.

    Args:
        version:

    Returns:

    """
    version_manager = get_from_version(version)
    try:
        version_manager.restore_version(version)
    except ValueError as value_error:
        raise ApiError('Unable to restore this version: status is not disabled.')
    return upsert(version_manager)


def disable_version(version, new_current=None):
    """Disable a version of the object, then saves it.

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
    """Set the current version of the object, then saves it.

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
    """Get the current version of the version manager.

    Args:
        version_manager:

    Returns:

    """
    return version_manager.current


def upsert(version_manager):
    """Save or update version manager.

    Args:
        version_manager:

    Returns:

    """
    return version_manager.save_version_manager()


def insert_version(version_manager, version):
    """Insert a version in the version manager, then saves it.

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
    """Return all Version Managers with user set to None.

    Returns:

    """
    return VersionManager.get_global_version_managers()


def get_active_global_version_manager_by_title(version_manager_title):
    """Return active Version Manager by its title with user set to None.

    Args:
        version_manager_title: Version Manager title

    Returns:
        Version Manager instance

    """
    return VersionManager.get_active_global_version_manager_by_title(version_manager_title)


def get_version_number(version_manager, version):
    """Return version number from version id.

    Args:
        version_manager:
        version:

    Returns:

    """
    return version_manager.get_version_number(version)


def get_version_by_number(version_manager, version_number):
    """Return the version by its version number.

    Args:
        version_manager:
        version_number: Number of the version.

    Returns:

    """
    return version_manager.get_version_by_number(version_number)
