""" Set of functions to define the rules for access control
"""

import core_main_app.permissions.rights as rights
from core_main_app.components.workspace import api as workspace_api
from core_main_app.permissions import api as permissions_api
from core_main_app.settings import CAN_SET_PUBLIC_DATA_TO_PRIVATE, CAN_ANONYMOUS_ACCESS_PUBLIC_DATA
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.raw_query.mongo_raw_query import add_access_criteria, \
    add_aggregate_access_criteria


def has_perm_publish_data(user):
    """ Does the user have the permission to publish a data.

    Args:
        user

    Returns
    """
    publish_perm = permissions_api.get_by_codename(rights.publish_data)
    if not user.has_perm(publish_perm.content_type.app_label + '.' + publish_perm.codename):
        raise AccessControlError("The user doesn't have enough rights to publish this " + get_data_label() + ".")


def has_perm_administration(func, *args, **kwargs):
    """ Is the given user has administration rights.

        Args:
            func:
            *args:
            **kwargs:

        Returns:

        """
    try:
        if args[0].is_superuser:
            return func(*args, **kwargs)
    except Exception:
        pass
    raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")


def can_read_or_write_data_workspace(func, workspace, user):
    """ Can user read or write in workspace.

    Args:
        func:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(workspace, user)

    _check_can_read_or_write_workspace(workspace, user)
    return func(workspace, user)


def can_write_data_workspace(func, data, workspace, user):
    """ Can user write data in workspace.

    Args:
        func:
        data:
        workspace:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data, workspace, user)
    if workspace is not None:
            if workspace_api.is_workspace_public(workspace):
                has_perm_publish_data(user)
            else:
                _check_can_write_workspace(workspace, user)

    check_can_write_data(data, user)

    # if we can not unpublish data
    if CAN_SET_PUBLIC_DATA_TO_PRIVATE is False:
        # if data is in public workspace
        if data.workspace is not None and workspace_api.is_workspace_public(data.workspace):
            # if target workspace is private
            if workspace is None or workspace_api.is_workspace_public(workspace) is False:
                raise AccessControlError("The " + get_data_label() + " can not be unpublished.")

    return func(data, workspace, user)


def _check_can_write_workspace(workspace, user):
    """ Check that user can write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    if workspace not in accessible_workspaces:
        raise AccessControlError("The user does not have the permission to write into this workspace.")


def _check_can_read_or_write_workspace(workspace, user):
    """ Check that user can read or write in the workspace.

    Args:
        workspace:
        user:

    Returns:

    """
    accessible_write_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    accessible_read_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
    if workspace not in list(accessible_write_workspaces) + list(accessible_read_workspaces):
        raise AccessControlError("The user does not have the permission to write into this workspace.")


def can_read_list_data_id(func, list_data_id, user):
    """ Can read list of data.

    Args:
        func:
        list_data_id:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(list_data_id, user)

    list_data = func(list_data_id, user)
    _check_can_read_data_list(list_data, user)

    return list_data


def can_read_data_id(func, data_id, user):
    """ Can read data.

    Args:
        func:
        data_id:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data_id, user)

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
    if user.is_superuser:
        return func(data, user)

    check_can_write_data(data, user)
    return func(data, user)


def can_read_data(func, data, user):
    """ Can read data.

    Args:
        func:
        data:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data, user)

    _check_can_read_data(data, user)
    return func(data, user)


def can_read_data_query(func, query, user, order_by_field=None):
    """ Can read a data, given a query.

    Args:
        func:
        query:
        user:
        order_by_field

    Returns:

    """
    if user.is_superuser:
        return func(query, user, order_by_field)

    # update the query
    query = _update_can_read_query(query, user)
    # get list of data
    data_list = func(query, user, order_by_field)
    # TODO: check if necessary because it is time consuming (checking that user has access to list of returned data)
    # check that user can access the list of data
    _check_can_read_data_list(data_list, user)
    return data_list


def can_read_aggregate_query(func, query, user):
    """ Can read a data, given an aggregate query.

    Args:
        func:
        query:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(query, user)

    # update the query
    query = _update_can_read_aggregate_query(query, user)
    # get list of data
    data = func(query, user)

    return data


def can_read_user(func, user):
    """ Can read data, given a user.

    Args:
        func:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(user)

    # get list of data
    data_list = func(user)
    # check that the user can access the list of data
    _check_can_read_data_list(data_list, user)
    # return list of data
    return data_list


def can_change_owner(func, data, new_user, user):
    """ Can user change data's owner.

    Args:
        func:
        data:
        new_user:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(data, new_user, user)

    if data.user_id != str(user.id):
        raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")

    return func(data, new_user, user)


def check_can_write_data(data, user):
    """ Check that the user can write a data.

    Args:
        data:
        user:

    Returns:

    """
    if data.user_id != str(user.id):
        if hasattr(data, 'workspace') and data.workspace is not None:
            # get list of accessible workspaces
            accessible_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
            # check that accessed data belongs to an accessible workspace
            if data.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")
        # workspace is not set
        else:
            raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")


def _check_can_read_data(data, user):
    """ Check that the user can read a data.

    Args:
        data:
        user:

    Returns:

    """
    # workspace case
    if data.user_id != str(user.id):
        # workspace is set
        if hasattr(data, 'workspace') and data.workspace is not None:
            # get list of accessible workspaces
            accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
            # check that accessed data belongs to an accessible workspace
            if data.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")
        # workspace is not set
        else:
            raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")


def _check_can_read_data_list(data_list, user):
    """ Check that the user can read each data of the list.

    Args:
        data_list:
        user:

    Returns:

    """
    if len(data_list) > 0:
        # get list of accessible workspaces
        accessible_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
        # check access is correct
        for data in data_list:
            # user is data owner
            if data.user_id == str(user.id):
                continue
            # user is not owner or data not in accessible workspace
            if data.workspace is None or data.workspace not in accessible_workspaces:
                raise AccessControlError("The user doesn't have enough rights to access this " + get_data_label() + ".")


def _update_can_read_query(query, user):
    """ Update query with access control parameters.

    Args:
        query:
        user:

    Returns:

    """

    accessible_workspaces = _get_read_accessible_workspaces_by_user(user)
    # update query with workspace criteria
    query = add_access_criteria(query, accessible_workspaces, user)
    return query


def _update_can_read_aggregate_query(query, user):
    """ Update query with access control parameters.

    Args:
        query:
        user:

    Returns:

    """

    accessible_workspaces = _get_read_accessible_workspaces_by_user(user)
    # update query with workspace criteria
    query = add_aggregate_access_criteria(query, accessible_workspaces, user)
    return query


def _get_read_accessible_workspaces_by_user(user):
    """ Get read accessible workspaces by user.

    Args:
        user:

    Returns:

    """
    if not CAN_ANONYMOUS_ACCESS_PUBLIC_DATA and user.is_anonymous:
        accessible_workspaces = []
    else:
        # workspace case
        # list accessible workspaces
        accessible_workspaces = [workspace.id for workspace in
                                 workspace_api.get_all_workspaces_with_read_access_by_user(user)]

    return accessible_workspaces
