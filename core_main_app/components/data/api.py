""" Data API
"""
import datetime

import pytz

import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from core_main_app.access_control import api as access_control_api
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data import access_control as data_api_access_control
from core_main_app.components.data.models import Data
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.xml import validate_xml_data
from core_main_app.settings import DATA_SORTING_FIELDS
from xml_utils.xsd_tree.xsd_tree import XSDTree


@access_control(access_control_api.can_read_or_write_in_workspace)
def get_all_by_workspace(workspace, user, order_by_field=DATA_SORTING_FIELDS):
    """ Get all data that belong to the workspace.

    Args:
        workspace:
        order_by_field:

    Returns:

    """
    return Data.get_all_by_workspace(workspace, order_by_field)


@access_control(data_api_access_control.can_read_list_data_id)
def get_by_id_list(list_data_id, user, order_by_field=DATA_SORTING_FIELDS):
    """ Return a list of data object with the given list id.

        Parameters:
            list_data_id:
            user:
            order_by_field:

        Returns: data object
    """
    return Data.get_all_by_id_list(list_data_id, order_by_field)


@access_control(core_main_app.access_control.api.can_read_id)
def get_by_id(data_id, user):
    """ Return data object with the given id.

        Parameters:
            data_id:
            user:

        Returns: data object
    """
    return Data.get_by_id(data_id)


@access_control(access_control_api.has_perm_administration)
def get_all(user, order_by_field=DATA_SORTING_FIELDS):
    """ Get all the data if superuser. Raise exception otherwise.

    Parameters:
            user:
            order_by_field: Order by field.

    Returns: data collection
    """
    return Data.get_all(order_by_field)


def get_all_accessible_by_user(user, order_by_field=DATA_SORTING_FIELDS):
    """ Return all data accessible by a user.

        Parameters:
            user:
            order_by_field:

        Returns: data collection
    """

    read_workspaces = workspace_api.get_all_workspaces_with_read_access_by_user(user)
    write_workspaces = workspace_api.get_all_workspaces_with_write_access_by_user(user)
    user_accessible_workspaces = list(set().union(read_workspaces, write_workspaces))

    return Data.get_all_by_user_and_workspace(user.id, user_accessible_workspaces, order_by_field)


def get_all_by_user(user, order_by_field=DATA_SORTING_FIELDS):
    """ Return all data owned by a user.

        Parameters:
            user:
            order_by_field: Order by field.

        Returns: data collection
    """
    return Data.get_all_by_user_id(str(user.id), order_by_field)


@access_control(core_main_app.access_control.api.can_read)
def get_all_except_user(user, order_by_field=DATA_SORTING_FIELDS):
    """ Return all data which are not created by the user.

        Parameters:
             user:
             order_by_field:

        Returns: data collection
    """
    return Data.get_all_except_user_id(str(user.id), order_by_field)


@access_control(core_main_app.access_control.api.can_write)
def upsert(data, user):
    """ Save or update the data.

    Args:
        data:
        user:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    data.last_modification_date = datetime.datetime.now(pytz.utc)
    check_xml_file_is_valid(data)
    return data.convert_and_save()


def check_xml_file_is_valid(data):
    """ Check if xml data is valid against a given schema.

    Args:
        data:

    Returns:

    """
    template = data.template

    try:
        xml_tree = XSDTree.build_tree(data.xml_content)
    except Exception as e:
        raise exceptions.XMLError(str(e))

    try:
        xsd_tree = XSDTree.build_tree(template.content)
    except Exception as e:
        raise exceptions.XSDError(str(e))

    error = validate_xml_data(xsd_tree, xml_tree)
    if error is not None:
        raise exceptions.XMLError(error)
    else:
        return True


@access_control(data_api_access_control.can_read_data_query)
def execute_query(query, user, order_by_field=DATA_SORTING_FIELDS):
    """Execute a query on the Data collection.

    Args:
        query:
        user:
        order_by_field:

    Returns:

    """
    return Data.execute_query(query, order_by_field)


@access_control(core_main_app.access_control.api.can_write)
def delete(data, user):
    """ Delete a data.

    Args:
        data:
        user:

    Returns:

    """
    data.delete()


@access_control(access_control_api.can_change_owner)
def change_owner(data, new_user, user):
    """ Change data's owner.

    Args:
        data:
        user:
        new_user:

    Returns:
    """
    # FIXME: user can transfer data to anybody, too permissive
    data.user_id = str(new_user.id)
    data.save()


def is_data_public(data):
    """ Is data public.

    Args:
        data:

    Returns:
    """
    return workspace_api.is_workspace_public(data.workspace) if data.workspace is not None else False


@access_control(data_api_access_control.can_read_aggregate_query)
def aggregate(pipeline, user):
    """Execute an aggregate on the Data collection.

    Args:
        pipeline:
        user:

    Returns:

    """
    return Data.aggregate(pipeline)


@access_control(data_api_access_control.can_write_data_workspace)
def assign(data, workspace, user):
    """ Assign blob to a workspace.

    Args:
        data:
        workspace:
        user:

    Returns:

    """
    data.workspace = workspace
    return data.save()
