""" Workspace access control
"""
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.permissions import api as permissions_api, rights as rights
from core_main_app.settings import CAN_SET_PUBLIC_DATA_TO_PRIVATE


def is_workspace_owner_to_perform_action_for_others(
    func, workspace, new_user_id, user
):
    """Check if the user is the owner of the workspace to perform action for other user.

    Args:
        func
        workspace
        new_user_id
        user

    Returns:

    """
    if user.is_superuser:
        return func(workspace, new_user_id, user)

    _check_is_owner_workspace(workspace, user)
    return func(workspace, new_user_id, user)


def can_user_set_workspace_public(func, workspace, user):
    """Check if the user is the owner of the workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_is_owner_workspace(workspace, user)

    publish_perm = permissions_api.get_by_codename(rights.PUBLISH_DATA)
    if not user.has_perm(
        publish_perm.content_type.app_label + "." + publish_perm.codename
    ):
        raise AccessControlError(
            "You don't have enough rights to set public this workspace."
        )

    return func(workspace, user)


def is_workspace_owner(func, workspace, user):
    """Check if the user is the owner of the workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_is_owner_workspace(workspace, user)
    return func(workspace, user)


def can_delete_workspace(func, workspace, user):
    """Can user delete a workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_is_owner_workspace(workspace, user)

    if CAN_SET_PUBLIC_DATA_TO_PRIVATE is False:
        if workspace.is_public:
            raise AccessControlError("The workspace can not be deleted.")

    return func(workspace, user)


def _check_is_owner_workspace(workspace, user):
    """Check that user is the owner of the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    if workspace.owner != str(user.id):
        raise AccessControlError(
            "The user does not have the permission. The user is not the owner of this workspace."
        )
