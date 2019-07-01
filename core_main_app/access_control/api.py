""" Set of functions to define the common rules for access control across collections
"""
import logging

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.workspace import api as workspace_api
from core_main_app.permissions import api as permissions_api
from core_main_app.settings import CAN_SET_PUBLIC_DATA_TO_PRIVATE

logger = logging.getLogger(__name__)


def can_read(func, user):
    """ Can a user read

    Args:
        func:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(user)

    # get list of item
    item_list = func(user)
    # check that the user can access the list of item
    check_can_read_list(item_list, user)
    # return list of item
    return item_list


def can_read_id(func, item_id, user):
    """ Can read from object if.

    Args:
        func:
        item_id:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(item_id, user)

    item = func(item_id, user)
    _check_can_read(item, user)
    return item


def can_write(func, item, user):
    """ Can user write

    Args:
        func:
        item:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(item, user)

    check_can_write(item, user)
    return func(item, user)


def can_read_or_write_in_workspace(func, workspace, user):
    """ Can user read or write in workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_can_read_or_write_in_workspace(workspace, user)
    return func(workspace, user)


def can_write_in_workspace(func, item, workspace, user, codename):
    """ Can user write in workspace.

    Args:
        func:
        item:
        workspace:
        user:
        codename:

    Returns:

    """
    if user.is_superuser:
        return func(item, workspace, user)
    if workspace is not None:
            if workspace_api.is_workspace_public(workspace):
                has_perm_publish(user, codename)
            else:
                _check_can_write_in_workspace(workspace, user)

    check_can_write(item, user)

    # if we can not unpublish
    if CAN_SET_PUBLIC_DATA_TO_PRIVATE is False:
        # if item is in public workspace
        if item.workspace is not None and workspace_api.is_workspace_public(item.workspace):
            # if target workspace is private
            if workspace is None or workspace_api.is_workspace_public(workspace) is False:
                raise AccessControlError("The document can not be unpublished.")

    return func(item, workspace, user)


def has_perm_publish(user, codename):
    """ Does the user have the permission to publish.

    Args:
        user
        codename

    Returns
    """
    publish_perm = permissions_api.get_by_codename(codename)
    if not user.has_perm(publish_perm.content_type.app_label + '.' + publish_perm.codename):
        raise AccessControlError("The user doesn't have enough rights to publish.")


def has_perm_administration(func, *args, **kwargs):
    """ Is the given user has administration rights.

        Args:
            func:
            *args:
            **kwargs:

        Returns:

        """
    try:
        if args[0].is_superuser:
            return func(*args, **kwargs)
    except Exception as e:
        logger.warning("has_perm_administration threw an exception: ".format(str(e)))

    raise AccessControlError("The user doesn't have enough rights.")


def check_can_write(item, user):
    """ Check that the user can write.

    Args:
        item:
        user:

    Returns:

    """
    if item.user_id != str(user.id):
        if hasattr(item, 'workspace') and item.workspace is not None:
            # get list of accessible workspaces
            accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
            # check that accessed item belongs to an accessible workspace
            if item.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights.")
        # workspace is not set
        else:
            raise AccessControlError("The user doesn't have enough rights.")


def check_can_read_list(item_list, user):
    """ Check that the user can read each item of the list.

    Args:
        item_list:
        user:

    Returns:

    """
    if len(item_list) > 0:
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # check access is correct
        for item in item_list:
            # user is item owner
            if item.user_id == str(user.id):
                continue
            # user is not owner or item not in accessible workspace
            if item.workspace is None or item.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights.")


def _check_can_write_in_workspace(workspace, user):
    """ Check that user can write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    if workspace not in accessible_workspaces:
        raise AccessControlError("The user does not have the permission to write into this workspace.")


def _check_can_read_or_write_in_workspace(workspace, user):
    """ Check that user can read or write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_write_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    accessible_read_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
    if workspace not in list(accessible_write_workspaces) + list(accessible_read_workspaces):
        raise AccessControlError("The user does not have the permission to write into this workspace.")


def _check_can_read(item, user):
    """ Check that the user can read.

    Args:
        item:
        user:

    Returns:

    """
    # workspace case
    if item.user_id != str(user.id):
        # workspace is set
        if hasattr(item, 'workspace') and item.workspace is not None:
            # get list of accessible workspaces
            accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
            # check that accessed item belongs to an accessible workspace
            if item.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights to access this.")
        # workspace is not set
        else:
            raise AccessControlError("The user doesn't have enough rights to access this.")
