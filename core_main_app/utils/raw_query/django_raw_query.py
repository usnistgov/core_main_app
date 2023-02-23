"""Utils for Django raw query
"""

from django.conf import settings

from core_main_app.utils.raw_query.common import (
    check_user_filter,
    check_workspace_filter,
)


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
    query &= access_criteria
    # return query
    return query


def _get_accessible_criteria(
    accessible_workspaces, user, workspace_filter=None, user_filter=None
):
    """Get accessible criteria.

    Args:
        accessible_workspaces:
        user:
        workspace_filter:
        user_filter:

    Returns:

    """
    if settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q

        workspace_key = "_workspace_id"
    else:
        from django.db.models import Q

        workspace_key = "workspace"
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
            query_filter &= Q(user_id__in=user_filter)
        # return the query
        return query_filter

    # check if user can filter by user
    check_user_filter(user_filter, user)
    # check if user can filter by workspace
    check_workspace_filter(workspace_filter, accessible_workspaces)

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
    access_criteria = Q(**{f"{workspace_key}__in": workspace_query})
    # if only workspace filter set, return access criteria
    if workspace_filter and not user_filter:
        return access_criteria
    # if connected user making the query
    if user and user.id:
        # if user filter is set
        if user_filter:
            # filter on user id
            access_criteria &= Q(user_id=str(user.id))
        else:
            # otherwise include user's own data to results
            access_criteria |= Q(user_id=str(user.id))
    # return access criteria
    return access_criteria


def get_workspace_query(list_workspace):
    """Return Q object to match list of workspaces

    Args:
        list_workspace:

    Returns:

    """
    if settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q

        workspace_key = "_workspace_id"
    else:
        from django.db.models import Q

        workspace_key = "workspace"

    # create initial query that returns all workspaces
    if len(list_workspace) == 0:
        return Q(**{f"{workspace_key}__in": []})
    # create empty query
    workspace_q_list = Q()
    for workspace_id in list_workspace:
        # if workspace id is None
        if workspace_id is None:
            # add query: OR workspace is null
            workspace_q_list |= Q(**{f"{workspace_key}__exact": None})
        else:  # workspace is not null
            # add query: OR workspace is equal to id
            workspace_q_list |= Q(**{f"{workspace_key}__exact": workspace_id})
    # return query
    return workspace_q_list
