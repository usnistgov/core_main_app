"""
Version Manager API
"""
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.version_manager.access_control import (
    can_read,
    can_write,
    can_read_global,
    can_read_list,
    can_read_version_manager,
)
from core_main_app.components.version_manager.models import VersionManager


@access_control(can_read)
def get(version_manager_id, request):
    """Get a version manager by its id.

    Args:
        version_manager_id:
        request:

    Returns:

    """
    return VersionManager.get_by_id(version_manager_id)


@access_control(can_read_list)
def get_by_id_list(list_id, request):
    """Get a version managers with the given id list.

    Args:
        list_id:
        request

    Returns:

    """
    return VersionManager.get_by_id_list(list_id)


@access_control(can_read)
def get_from_version(version, request):
    """Return a version manager from a version.

    Args:
        version:
        request:

    Returns:

    """
    version_managers = VersionManager.get_all()
    for version_manager in version_managers:
        if str(version.id) in version_manager.versions:
            return version_manager
    raise exceptions.ApiError("No version manager could be found for this version.")


# NOTE: access control by upsert
def disable(version_manager, request):
    """Disable an object, then saves it.

    Args:
        version_manager:
        request:

    Returns:

    """
    version_manager.disable()
    return upsert(version_manager, request=request)


# NOTE: access control by upsert
def restore(version_manager, request):
    """Restore an object, then saves it.

    Args:
        version_manager:
        request:

    Returns:

    """
    version_manager.restore()
    return upsert(version_manager, request=request)


# NOTE: access control by upsert
def restore_version(version, request):
    """Disable a version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    version_manager = get_from_version(version, request=request)
    try:
        version_manager.restore_version(version)
    except ValueError:
        raise ApiError("Unable to restore this version: status is not disabled.")
    return upsert(version_manager, request=request)


# NOTE: access control by upsert
def disable_version(version, request, new_current=None):
    """Disable a version of the object, then saves it.

    Args:
        version:
        new_current:
        request:

    Returns:

    """
    version_manager = get_from_version(version, request=request)

    # try to delete the current version
    if version_manager.current == str(version.id):
        # no version to be current provided
        if new_current is None:
            raise exceptions.ApiError("Unable to disable the current version.")

        # id doesn't match a version
        if new_current.id not in version_manager.versions:
            raise exceptions.ApiError(
                "The id provided to be the next current version, could not be found.",
            )

        # set the new current version
        version_manager.set_current_version(new_current)

    # disable the version
    version_manager.disable_version(version)
    return upsert(version_manager, request=request)


# NOTE: access control by upsert
def set_current(version, request):
    """Set the current version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    version_manager = get_from_version(version, request=request)

    # a disabled version cannot be current
    if str(version.id) in version_manager.get_disabled_versions():
        raise exceptions.ApiError(
            "Unable to set the current version because it is disabled."
        )

    version_manager.set_current_version(version)
    return upsert(version_manager, request=request)


@access_control(can_write)
def upsert(version_manager, request):
    """Save or update version manager.

    Args:
        version_manager:
        request:

    Returns:

    """
    return version_manager.save_version_manager()


# NOTE: access control by upsert
def insert_version(version_manager, version, request):
    """Insert a version in the version manager, then saves it.

    Args:
        version_manager:
        version:
        request:

    Returns:

    """
    version_manager.insert(version)

    # first version inserted, set it as current
    if len(version_manager.versions) == 1:
        version_manager.set_current_version(version)

    return upsert(version_manager, request=request)


@access_control(can_read_global)
def get_active_global_version_manager_by_title(version_manager_title, request):
    """Return active Version Manager by its title with user set to None.

    Args:
        version_manager_title: Version Manager title
        request:

    Returns:
        Version Manager instance

    """
    return VersionManager.get_active_global_version_manager_by_title(
        version_manager_title
    )


@access_control(can_read_version_manager)
def get_version_number(version_manager, version, request):
    """Return version number from version id.

    Args:
        version_manager:
        version:
        request:

    Returns:

    """
    return version_manager.versions.index(str(version)) + 1


@access_control(can_read_version_manager)
def get_version_by_number(version_manager, version_number, request):
    """Return the version by its version number.

    Args:
        version_manager:
        version_number: Number of the version
        request:

    Returns:

    """
    return version_manager.versions[version_number - 1]
