"""
Version Manager API
"""

from core_main_app.commons.exceptions import MDCSError
from core_main_app.components.version_manager.models import VersionManager


def vm_get(vm_id):
    """
    Get a version manager by its id
    :param vm_id:
    :return:
    """
    try:
        return VersionManager.get_by_id(vm_id)
    except:
        raise MDCSError('No version manager could be found with the given id')


def vm_get_from_version(version_id):
    """
    Return VM from a version id
    :param version_id:
    :return:
    """
    version_managers = VersionManager.get_all_version_managers()
    for version_manager in version_managers:
        if str(version_id) in version_manager.versions:
            return version_manager
    raise MDCSError("No version manager could be found for this id.")


def vm_disable(version_manager_id):
    """
    Disable an object
    :param version_manager_id:
    :return:
    """
    vm = vm_get(version_manager_id)
    vm.disable()


def vm_restore(version_manager_id):
    """
    Restore an object
    :param version_manager_id:
    :return:
    """
    vm = vm_get(version_manager_id)
    vm.restore()


def vm_restore_version(version_id):
    """
    Disable a version of the object
    :param version_id:
    :return:
    """
    vm = vm_get_from_version(version_id)
    vm.restore_version(version_id)


def vm_disable_version(version_id, new_current_id=None):
    """
    Disable a version of the object
    :param version_id:
    :param new_current_id:
    :return:
    """
    vm = vm_get_from_version(version_id)

    # try to delete the current version
    if vm.current == str(version_id):
        # no version to be current provided
        if new_current_id is None:
            raise MDCSError('Unable to disable the current version.')

        # id doesn't match a version
        if new_current_id not in vm.versions:
            raise MDCSError('The id provided to be the next current version, could not be found.')

        # set the new current version
        vm.set_current_version(new_current_id)
        # disable the version
        vm.disable_version(version_id)

    # try to delete another version than the current
    else:
        # disable the version
        vm.disable_version(version_id)


def vm_set_current(version_id):
    """
    Set the current version of the object
    :param version_id:
    :return:
    """
    vm = vm_get_from_version(version_id)
    vm.set_current_version(version_id)


def vm_get_current(vm_id):
    """
    Get the current version of the version manager
    :param vm_id:
    :return:
    """
    vm = vm_get(vm_id)
    return vm.current
