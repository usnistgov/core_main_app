"""
Version Manager API
"""

from core_main_app.commons import exceptions
from core_main_app.components.version_manager.models import VersionManager


def get(version_manager_id):
    """
    Get a version manager by its id
    :param version_manager_id:
    :return:
    """
    try:
        return VersionManager.get_by_id(version_manager_id)
    except:
        raise exceptions.ApiError('No version manager could be found with the given id')


def get_from_version(version_id):
    """
    Return VM from a version id
    :param version_id:
    :return:
    """
    version_managers = VersionManager.get_all()
    for version_manager in version_managers:
        if str(version_id) in version_manager.versions:
            return version_manager
    raise exceptions.ApiError("No version manager could be found for this id.")


def disable(version_manager_id):
    """
    Disable an object
    :param version_manager_id:
    :return:
    """
    version_manager = get(version_manager_id)
    version_manager.disable()


def restore(version_manager_id):
    """
    Restore an object
    :param version_manager_id:
    :return:
    """
    version_manager = get(version_manager_id)
    version_manager.restore()


def restore_version(version_id):
    """
    Disable a version of the object
    :param version_id:
    :return:
    """
    version_manager = get_from_version(version_id)
    version_manager.restore_version(version_id)


def disable_version(version_id, new_current_id=None):
    """
    Disable a version of the object
    :param version_id:
    :param new_current_id:
    :return:
    """
    version_manager = get_from_version(version_id)

    # try to delete the current version
    if version_manager.current == str(version_id):
        # no version to be current provided
        if new_current_id is None:
            raise exceptions.ApiError('Unable to disable the current version.')

        # id doesn't match a version
        if new_current_id not in version_manager.versions:
            raise exceptions.ApiError('The id provided to be the next current version, could not be found.')

        # set the new current version
        version_manager.set_current_version(new_current_id)
        # disable the version
        version_manager.disable_version(version_id)

    # try to delete another version than the current
    else:
        # disable the version
        version_manager.disable_version(version_id)


def set_current(version_id):
    """
    Set the current version of the object
    :param version_id:
    :return:
    """
    version_manager = get_from_version(version_id)
    version_manager.set_current_version(version_id)


def get_current(version_manager_id):
    """
    Get the current version of the version manager
    :param version_manager_id:
    :return:
    """
    version_manager = get(version_manager_id)
    return version_manager.current


def update_title(version_manager_id, title):
    """
    Update version manager's title
    :param version_manager_id:
    :param title:
    :return:
    """
    version_manager = get(version_manager_id)
    version_manager.title = title
    return version_manager.save()
