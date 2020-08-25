""" Set of functions to define the rules for access control
"""
import logging

import core_main_app.permissions.rights as rights
from core_main_app.access_control.api import (
    has_perm_publish,
    check_can_read_list,
    can_write_in_workspace,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.workspace import api as workspace_api
from core_main_app.settings import (
    CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT,
    VERIFY_DATA_ACCESS,
)
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.raw_query.mongo_raw_query import (
    add_access_criteria,
    add_aggregate_access_criteria,
)
from core_main_app.settings import DATA_SORTING_FIELDS

logger = logging.getLogger(__name__)


def has_perm_publish_data(user):
    """Does the user have the permission to publish a data.

    Args:
        user

    Returns
    """
    has_perm_publish(user, rights.publish_data)


def can_read_list_data_id(func, list_data_id, user):
    """Can read list of data.

    Args:
        func:
        list_data_id:
        user:

    Returns:

    """
    if user.is_superuser:
        return func(list_data_id, user)

    list_data = func(list_data_id, user)
    check_can_read_list(list_data, user)

    return list_data


def can_read_data_query(func, query, user, order_by_field=DATA_SORTING_FIELDS):
    """Can read a data, given a query.

    Args:
        func:
        query:
        user:
        order_by_field:

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
    if VERIFY_DATA_ACCESS:
        check_can_read_list(data_list, user)
    return data_list


def can_read_aggregate_query(func, query, user):
    """Can read a data, given an aggregate query.

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


def _update_can_read_query(query, user):
    """Update query with access control parameters.

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
    """Update query with access control parameters.

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
    """Get read accessible workspaces by user.

    Args:
        user:

    Returns:

    """
    if not CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT and user.is_anonymous:
        accessible_workspaces = []
    else:
        # workspace case
        # list accessible workspaces
        accessible_workspaces = [
            workspace.id
            for workspace in workspace_api.get_all_workspaces_with_read_access_by_user(
                user
            )
        ]

    return accessible_workspaces


def can_write_data_workspace(func, data, workspace, user):
    """Can user write data in workspace.

    Args:
        func:
        data:
        workspace:
        user:

    Returns:

    """
    return can_write_in_workspace(func, data, workspace, user, rights.publish_data)
