""" System API allowing to perform call on Data without access control. Use this API carefully.
"""
from core_main_app.components.data.models import Data
from core_main_app.settings import DATA_SORTING_FIELDS


def get_data_by_id(data_id):
    """ Return data object with the given id.

        Parameters:
            data_id:

        Returns: data object
    """
    return Data.get_by_id(data_id)


def get_all_by_template(template, order_by_field=DATA_SORTING_FIELDS):
    """ Get all data belonging to the specified template.

    Args:
        template:
        order_by_field:

    Returns:

    """
    return Data.objects(template=template).order_by(order_by_field)


def get_all_by_list_template(list_template, order_by_field=DATA_SORTING_FIELDS):
    """ Get all data that belong to the template list.

    Args:
        list_template:
        order_by_field:

    Returns:

    """
    return Data.get_all_by_list_template(list_template, order_by_field)


def get_all_except(id_list, order_by_field=DATA_SORTING_FIELDS):
    """ Get all data except the ones with the IDs provided.

    Args:
        id_list:
        order_by_field:

    Returns:

    """
    return Data.get_all_except(order_by_field, id_list)


def execute_query_with_projection(query, projection, order_by_field=DATA_SORTING_FIELDS):
    """ Execute a given query with a projection.

    Args:
        query:
        projection:
        order_by_field:

    Returns:

    """
    return Data.execute_query(query, order_by_field).only(projection)
