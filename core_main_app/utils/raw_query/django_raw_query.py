"""Utils for Django raw query
"""

from django.db.models import Q

from core_main_app.access_control.exceptions import AccessControlError


def add_access_criteria(
    query, accessible_workspaces, user, workspace_filter=None, user_filter=None
):
    """Add access criteria to the query.

    Args:
        query:
        accessible_workspaces:
        user:
        workspace_filter:
        user_filter:

    Returns:

    """
    # get access criteria to update query
    access_criteria = _get_accessible_criteria(
        accessible_workspaces, user, workspace_filter, user_filter
    )
    # add access criteria to original query
    query = Q(access_criteria & query)
    # return query
    return query


def _get_accessible_criteria(
    accessible_workspaces, user, workspace_filter=None, user_filter=None
):
    """Get accessible criteria.

    Args:
        accessible_workspaces:
        user:

    Returns:

    """
    # if superuser don't check permissions, only apply filters
    if user.is_superuser:
        # create query
        query_filter = Q()
        # if workspaces provided
        if workspace_filter:
            # add filter by workspace
            query_filter &= get_workspace_query(workspace_filter)
        # if user ids provided
        if user_filter:
            # add filter by users
            query_filter &= Q(user_id__in=str(user_filter))
        # return the query
        return query_filter

    # if regular user does a query on other user id
    if user_filter and str(user_filter) != str(user.id):
        # raise access control error
        raise AccessControlError("The user does not have enough filter by user.")
    # iterate list of workspace filter provided
    for workspace in workspace_filter:
        # if workspace is not accessible
        if workspace not in accessible_workspaces:
            # raise access control error
            raise AccessControlError(
                "The user does not have enough right to filter by workspace."
            )

    # build workspace query: all accessible workspaces or only selected workspaces among accessible ones
    workspace_query = (
        [
            workspace
            for workspace in workspace_filter
            if workspace in accessible_workspaces
        ]
        if workspace_filter
        else accessible_workspaces
    )
    # workspace should be in list of accessible workspaces
    workspace_criteria = Q(workspace__in=workspace_query)
    # user_id should have the id of the user making the query
    user_criteria = Q(user_id=str(user.id))
    # access granted if workspace or user criteria true
    access_criteria = Q(workspace_criteria | user_criteria)
    # return access criteria
    return access_criteria


def get_workspace_query(list_workspace):
    """Return Q object to match list of workspaces

    Args:
        list_workspace:

    Returns:

    """
    # create initial query that returns all workspaces
    if len(list_workspace) == 0:
        return Q(workspace__in=[])
    # create empty query
    workspace_q_list = Q()
    for workspace_id in list_workspace:
        # if workspace id is None
        if workspace_id is None:
            # add query: OR workspace is null
            workspace_q_list |= Q(workspace__isnull=True)
        else:  # workspace is not null
            # add query: OR workspace is equal to id
            workspace_q_list |= Q(workspace=workspace_id)
    # return query
    return workspace_q_list
