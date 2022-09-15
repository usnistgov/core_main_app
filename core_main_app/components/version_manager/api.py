"""
Version Manager API
"""
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.version_manager.access_control import (
    can_write,
    can_read_version_manager,
)


@access_control(can_write)
def disable(version_manager, request):
    """Disable an object, then saves it.

    Args:
        version_manager:
        request:

    Returns:

    """
    version_manager.is_disabled = True
    version_manager.save()
    return version_manager


@access_control(can_write)
def restore(version_manager, request):
    """Restore an object, then saves it.

    Args:
        version_manager:
        request:

    Returns:

    """
    version_manager.is_disabled = False
    version_manager.save()
    return version_manager


@access_control(can_write)
def restore_version(version, request):
    """Disable a version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    if not version.is_disabled:
        raise ApiError("Unable to restore this version: status is not disabled.")
    version.is_disabled = False
    version.save()


@access_control(can_write)
def disable_version(version, request, new_current=None):
    """Disable a version of the object, then saves it.

    Args:
        version:
        new_current:
        request:

    Returns:

    """
    version_manager = version.version_manager

    # try to delete the current version
    if version.is_current:
        # no version to be current provided
        if new_current is None:
            raise exceptions.ApiError("Unable to disable the current version.")

        # id doesn't match a version
        if new_current.id not in version_manager.versions:
            raise exceptions.ApiError(
                "The id provided to be the next current version, could not be found.",
            )

        # set the new current version
        set_current(new_current, request)

    # disable the version
    version.is_disabled = True
    version.save()


@access_control(can_write)
def set_current(version, request):
    """Set the current version of the object, then saves it.

    Args:
        version:
        request:

    Returns:

    """
    version_manager = version.version_manager

    # a disabled version cannot be current
    if version.is_disabled:
        raise exceptions.ApiError(
            "Unable to set the current version because it is disabled."
        )

    # unset current version
    current_version = version_manager.current_version
    current_version.is_current = False
    current_version.save()

    # set version as current
    version.is_current = True
    version.save()
    return version  # NOTE: use to return version manager


@access_control(can_write)
def upsert(version_manager, request):
    """Save or update version manager.

    Args:
        version_manager:
        request:

    Returns:

    """
    return version_manager.save_version_manager()


@access_control(can_read_version_manager)
def get_version_number(version_manager, version_id, request):
    """Return version number from version id.

    Args:
        version_manager:
        version_id:
        request:

    Returns:

    """
    return list(version_manager.versions).index(str(version_id)) + 1


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
