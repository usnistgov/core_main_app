"""Utils for mongodb raw query
"""
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
    # check if user can filter by user
    check_user_filter(user_filter, user)
    # check if user can filter by workspace
    check_workspace_filter(workspace_filter, accessible_workspaces)
    # get access criteria query
    access_criteria = _get_accessible_criteria(accessible_workspaces, user)
    # add access criteria to original query
    query = {"$and": [query, access_criteria]}
    # return query
    return query


def add_aggregate_access_criteria(query, accessible_workspaces, user):
    """Add access criteria to an aggregation query.

    Args:
        query:
        accessible_workspaces:
        user:

    Returns:

    """
    has_match_criteria = False
    access_criteria = _get_accessible_criteria(accessible_workspaces, user)
    # Update $match with access criteria if exist.
    for elt in query:
        if "$match" in elt:
            elt["$match"].update(access_criteria)
            has_match_criteria = True
            break
    # Add $match with access criteria if does not exist.
    if not has_match_criteria:
        query.insert(0, {"$match": access_criteria})

    return query


def _get_accessible_criteria(accessible_workspaces, user):
    """Get accessible criteria.

    Args:
        accessible_workspaces:
        user:

    Returns:

    """
    # workspace should be in list of accessible workspaces
    workspace_criteria = {"workspace": {"$in": accessible_workspaces}}
    # user_id should have the id of the user making the query
    user_criteria = {"user_id": user.id}
    # access granted if workspace or user criteria true
    access_criteria = {"$or": [workspace_criteria, user_criteria]}
    # return access criteria
    return access_criteria
