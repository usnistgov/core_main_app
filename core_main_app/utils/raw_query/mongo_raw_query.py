"""Utils for mongodb raw query
"""


def add_access_criteria(query, accessible_workspaces, user):
    """ Add access criteria to the query.

    Args:
        query:
        accessible_workspaces:
        user:

    Returns:

    """
    # workspace should be in list of accessible workspaces
    workspace_criteria = {'workspace': {"$in": accessible_workspaces}}
    # user_id should have the id of the user making the query
    user_criteria = {'user_id': str(user.id)}
    # access granted if workspace or user criteria true
    access_criteria = {'$or': [workspace_criteria, user_criteria]}
    # add access criteria to original query
    query = {'$and': [query, access_criteria]}
    # return query
    return query
