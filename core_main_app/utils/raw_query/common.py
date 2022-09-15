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

    def _check_user(user_id_filter, user_id):
        """Raise ACL error if user_id_filter different from user id doing request

        Args:
            user_id_filter:
            user_id:

        Returns:

        """
        if user_id_filter and str(user_id_filter) != str(user_id):
            # raise access control error
            raise AccessControlError("The user does not have enough filter by user.")

    # if regular user does a query on other user id, raise access control error
    if isinstance(user_filter, list):
        for user_filter_id in user_filter:
            _check_user(user_filter_id, user.id)
    else:
        _check_user(user_filter, user.id)


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
