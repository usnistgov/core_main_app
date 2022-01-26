""" Raw queries common utils
"""

from core_main_app.access_control.exceptions import AccessControlError


def check_user_filter(user_filter, user):
    """Check that user is allowed to filter by user

    Args:
        user_filter:
        user:

    Returns:

    """
    # if regular user does a query on other user id
    if user_filter and str(user_filter) != str(user.id):
        # raise access control error
        raise AccessControlError("The user does not have enough filter by user.")


def check_workspace_filter(workspace_filter, accessible_workspaces):
    """Check that user is allowed to filter by list of workspaces

    Args:
        workspace_filter:
        accessible_workspaces:

    Returns:

    """
    # iterate list of workspace filter provided
    if workspace_filter:
        for workspace in workspace_filter:
            # if workspace is not accessible
            if workspace not in accessible_workspaces:
                # raise access control error
                raise AccessControlError(
                    "The user does not have enough right to filter by workspace."
                )
