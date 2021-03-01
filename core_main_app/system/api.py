""" System API allowing to perform call on Data without access control. Use this API carefully.
"""
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.version_manager.models import VersionManager
from core_main_app.settings import DATA_SORTING_FIELDS


def get_data_by_id(data_id):
    """Return data object with the given id.

    Parameters:
        data_id:

    Returns: data object
    """
    return Data.get_by_id(data_id)


def get_all_by_template(template, order_by_field=DATA_SORTING_FIELDS):
    """Get all data belonging to the specified template.

    Args:
        template:
        order_by_field:

    Returns:

    """
    return Data.objects(template=template).order_by(order_by_field)


def get_all_by_list_template(list_template, order_by_field=DATA_SORTING_FIELDS):
    """Get all data that belong to the template list.

    Args:
        list_template:
        order_by_field:

    Returns:

    """
    return Data.get_all_by_list_template(list_template, order_by_field)


def get_all_except(id_list, order_by_field=DATA_SORTING_FIELDS):
    """Get all data except the ones with the IDs provided.

    Args:
        id_list:
        order_by_field:

    Returns:

    """
    return Data.get_all_except(order_by_field, id_list)


def execute_query_with_projection(
    query, projection, order_by_field=DATA_SORTING_FIELDS
):
    """Execute a given query with a projection.

    Args:
        query:
        projection:
        order_by_field:

    Returns:

    """
    return Data.execute_query(query, order_by_field).only(projection)


def get_all_data_in_workspaces(workspace_list):
    """Get all data stored in a list of workspace

    Args:
        workspace_list:

    Returns:

    """
    return Data.get_all_by_list_workspace(workspace_list, DATA_SORTING_FIELDS)


def get_all_data_in_workspaces_for_templates(workspace_list, template_list):
    """Get all data stored in a list of workspace and validated by a list of
    templates

    Args:
        workspace_list:
        template_list:

    Returns:

    """
    return Data.get_all_by_templates_and_workspaces(
        template_list, workspace_list, DATA_SORTING_FIELDS
    )


def get_all_templates():
    """Return all templates

    Returns:

    """
    return Template.get_all(is_cls=True)


def get_template_by_id(template_id):
    """Get template by id

    Args:
        template_id:

    Returns:

    """
    return Template.get_by_id(template_id)


def upsert_data(data):
    """Upsert data

    Args:
        data:

    Returns:

    """
    from core_main_app.components.data.api import check_xml_file_is_valid

    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    check_xml_file_is_valid(data)
    return data.convert_and_save()


def get_active_global_version_manager_by_title(version_manager_title):
    """Get active global version manager by title

    Args:
        version_manager_title:

    Returns:

    """
    return VersionManager.get_active_global_version_manager_by_title(
        version_manager_title
    )
