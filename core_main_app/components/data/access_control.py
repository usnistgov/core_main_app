""" Set of functions to define the rules for access control
"""

from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.settings import INSTALLED_APPS
from core_main_app.utils.raw_query.mongo_raw_query import add_workspace_criteria

if 'core_workspace_app' in INSTALLED_APPS:
    from core_workspace_app.components.workspace import api as workspace_api


def can_read_data_id(func, data_id, user):
    """ Can read data.

    Args:
        func:
        data_id:
        user:

    Returns:

    """
    data = func(data_id, user)
    _check_can_read_data(data, user)
    return data


def can_write_data(func, data, user):
    """ Can write data.

    Args:
        func:
        data:
        user:

    Returns:

    """
    _check_can_write_data(data, user)
    return func(data, user)


def can_read_data(func, data, user):
    """ Can read data.

    Args:
        func:
        data:
        user:

    Returns:

    """
    _check_can_read_data(data, user)
    return func(data, user)


def can_read_data_query(func, query, user):
    """ Can read a data, given a query.

    Args:
        func:
        query:
        user:

    Returns:

    """
    # update the query
    query = _update_can_read_query(query, user)
    # get list of data
    data_list = func(query, user)
    # TODO: check if necessary because it is time consuming (checking that user has access to list of returned data)
    # check that user can access the list of data
    _check_can_read_data_list(data_list, user)
    return data_list


def can_read_user(func, user):
    """ Can read data, given a user.

    Args:
        func:
        user:

    Returns:

    """
    # get list of data
    data_list = func(user)
    # check that the user can access the list of data
    _check_can_read_data_list(data_list, user)
    # return list of data
    return data_list


def _check_can_write_data(data, user):
    """ Check that the user can write a data.

    Args:
        data:
        user:

    Returns:

    """
    # workspace case
    if 'core_workspace_app' in INSTALLED_APPS and hasattr(data, 'workspace') and data.workspace is not None:
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
        # check that accessed data belongs to an accessible workspace
        if data.workspace not in accessible_workspaces:
            raise AccessControlError("The user doesn't have enough rights to access this data")
    # general case
    else:
        # general case: admin and owner can write data
        if not user.is_staff:
            if data.user_id != str(user.id):
                raise AccessControlError("The user doesn't have enough rights to access this data")


def _check_can_read_data(data, user):
    """ Check that the user can read a data.

    Args:
        data:
        user:

    Returns:

    """
    # workspace case
    if 'core_workspace_app' in INSTALLED_APPS and hasattr(data, 'workspace') and data.workspace is not None:
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # check that accessed data belongs to an accessible workspace
        if data.workspace not in accessible_workspaces:
            raise AccessControlError("The user doesn't have enough rights to access this data")
    else:
        # general case: users can read other users data
        pass


def _check_can_read_data_list(data_list, user):
    """ Check that the user can read each data of the list.

    Args:
        data_list:
        user:

    Returns:

    """
    if 'core_workspace_app' in INSTALLED_APPS:
        # TODO: may not work if database was previously created without workspaces
        # get workspaces of list of data
        data_workspaces = set(data_list.values_list('workspace'))
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # check that accessed workspaces are in the list of accessible workspaces
        for workspace in data_workspaces:
            if workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights to access this data")
    else:
        # general case: users can read other users data
        pass


def _update_can_read_query(query, user):
    """ Update query with access control parameters.

    Args:
        query:
        user:

    Returns:

    """

    # workspace case
    if 'core_workspace_app' in INSTALLED_APPS:
        # list accessible workspaces
        accessible_workspaces = [workspace.id for workspace in
                                 workspace_api.get_all_workspaces_with_read_access_by_user(user)]
        # update query with workspace criteria
        query = add_workspace_criteria(query, accessible_workspaces)
    else:
        # general case: users can read other users data
        pass

    return query
