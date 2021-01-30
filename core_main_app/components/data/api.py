""" Data API
"""
import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from core_main_app.access_control import api as access_control_api
from core_main_app.access_control.api import has_perm_administration, is_superuser
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data import access_control as data_api_access_control
from core_main_app.components.data.models import Data
from core_main_app.components.data.tasks import (
    async_migration_task,
    async_template_migration_task,
)
from core_main_app.components.workspace import api as workspace_api
from core_main_app.settings import DATA_SORTING_FIELDS
from core_main_app.utils.datetime_tools.utils import datetime_now
from core_main_app.utils.xml import validate_xml_data
from xml_utils.xsd_tree.xsd_tree import XSDTree


@access_control(access_control_api.can_read_or_write_in_workspace)
def get_all_by_workspace(workspace, user, order_by_field=DATA_SORTING_FIELDS):
    """Get all data that belong to the workspace.

    Args:
        workspace:
        order_by_field:

    Returns:

    """
    return Data.get_all_by_workspace(workspace, order_by_field)


@access_control(data_api_access_control.can_read_list_data_id)
def get_by_id_list(list_data_id, user, order_by_field=DATA_SORTING_FIELDS):
    """Return a list of data object with the given list id.

    Parameters:
        list_data_id:
        user:
        order_by_field:

    Returns: data object
    """
    return Data.get_all_by_id_list(list_data_id, order_by_field)


@access_control(core_main_app.access_control.api.can_read_id)
def get_by_id(data_id, user):
    """Return data object with the given id.

    Parameters:
        data_id:
        user:

    Returns: data object
    """
    return Data.get_by_id(data_id)


@access_control(access_control_api.has_perm_administration)
def get_all(user, order_by_field=DATA_SORTING_FIELDS):
    """Get all the data if superuser. Raise exception otherwise.

    Parameters:
            user:
            order_by_field: Order by field.

    Returns: data collection
    """
    return Data.get_all(order_by_field)


def get_all_by_user(user, order_by_field=DATA_SORTING_FIELDS):
    """Return all data owned by a user.

    Parameters:
        user:
        order_by_field: Order by field.

    Returns: data collection
    """
    return Data.get_all_by_user_id(str(user.id), order_by_field)


@access_control(core_main_app.access_control.api.can_read)
def get_all_except_user(user, order_by_field=DATA_SORTING_FIELDS):
    """Return all data which are not created by the user.

    Parameters:
         user:
         order_by_field:

    Returns: data collection
    """
    return Data.get_all_except_user_id(str(user.id), order_by_field)


@access_control(core_main_app.access_control.api.can_request_write)
def upsert(data, request):
    """Save or update the data.

    Args:
        data:
        request:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    check_xml_file_is_valid(data, request=request)
    return data.convert_and_save()


@access_control(is_superuser)
def admin_insert(data, request):
    """Save the data.

    Args:
        data:
        request:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    # initialize times - use values if provided, set now otherwise
    now = datetime_now()
    if not data.creation_date:
        data.creation_date = now
    if not data.last_modification_date:
        data.last_modification_date = now
    if not data.last_change_date:
        data.last_change_date = now

    # convert and save the data (do not call convert_and_save that will set the date fields)
    check_xml_file_is_valid(data, request=request)
    data.convert_to_file()
    data.convert_to_dict()
    return data.save()


def check_xml_file_is_valid(data, request=None):
    """Check if xml data is valid against a given schema.

    Args:
        data:
        request:

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
    error = validate_xml_data(xsd_tree, xml_tree, request=request)
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
    """Delete a data.

    Args:
        data:
        user:

    Returns:

    """
    data.delete()


@access_control(access_control_api.can_change_owner)
def change_owner(data, new_user, user):
    """Change data's owner.

    Args:
        data:
        user:
        new_user:

    Returns:
    """
    # FIXME: user can transfer data to anybody, too permissive
    data.user_id = str(new_user.id)
    data.save_object()


def get_none():
    """Returns None object, used by data

    Returns:

    """
    return Data.get_none()


def is_data_public(data):
    """Is data public.

    Args:
        data:

    Returns:
    """
    return (
        workspace_api.is_workspace_public(data.workspace)
        if data.workspace is not None
        else False
    )


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
    """Assign blob to a workspace.

    Args:
        data:
        workspace:
        user:

    Returns:

    """
    data.workspace = workspace
    return data.save_object()


@access_control(has_perm_administration)
def migrate_data_list(data_list, target_template_id, migrate, user):
    """Perform a migration / validation of the data list for the given target template id
    NB: This action is executed with an async task, use the progress / result function to retrieve
    information about the task status

    Args:
        data_list:
        target_template_id:
        migrate: (boolean) Perform the migration
        user:

    Return:
        Async task id
    """
    task = async_migration_task.delay(
        data_list, str(target_template_id), user.id, migrate
    )
    return task.task_id


@access_control(has_perm_administration)
def migrate_template_list(template_id_list, target_template_id, migrate, user):
    """Perform a migration / validation of all the data which belong to the given template id list
    NB: This action is executed with an async task, use the progress / result function to retrieve
    information about the task status

    Args:
        template_id_list:
        target_template_id:
        migrate: (boolean) Perform the migration
        user:

    Return:
        Async task id
    """
    task = async_template_migration_task.delay(
        template_id_list, str(target_template_id), user.id, migrate
    )
    return task.task_id
