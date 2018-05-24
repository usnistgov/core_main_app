"""
    Workspace access control
"""
from core_main_app.settings import CAN_SET_PUBLIC_DATA_TO_PRIVATE
from core_main_app.utils.access_control.exceptions import AccessControlError


def is_workspace_owner_to_perform_action_for_others(func, workspace, new_user_id, user):
    """ Check if the user is the owner of the workspace to perform action for other user.

    Args:
        func
        workspace
        new_user_id
        user

    Returns:

    """
    if user.is_superuser:
        return func(workspace, new_user_id, user)

    _check_is_owner_workspace(workspace,  user)
    return func(workspace, new_user_id, user)


def is_workspace_owner(func, workspace, user):
    """ Check if the user is the owner of the workspace.

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
    """ Can user delete a workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_is_owner_workspace(workspace, user)

    # FIXME: uncomment when is_public is added to model
    # if CAN_SET_PUBLIC_DATA_TO_PRIVATE is False:
    #     if workspace.is_public:
    #         raise AccessControlError("The workspace can not be delete.")

    return func(workspace, user)


def _check_is_owner_workspace(workspace, user):
    """ Check that user is the owner of the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    if workspace.owner != str(user.id):
        raise AccessControlError("The user does not have the permission. The user is not the owner of this workspace.")
