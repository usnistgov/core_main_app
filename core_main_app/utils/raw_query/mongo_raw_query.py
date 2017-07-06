"""Utils for mongodb raw query
"""


def add_workspace_criteria(query, accessible_workspaces):
    """ Add a workspace criteria to the query.

    Args:
        query:
        accessible_workspaces:

    Returns:

    """
    workspace_criteria = {'workspace': {"$in": accessible_workspaces}}
    query = {'$and': [query, workspace_criteria]}
    return query
