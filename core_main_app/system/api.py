""" System API allowing to perform call on Data without access control. Use this API carefully.
"""
from core_main_app.components.data.models import Data


def get_data_by_id(data_id):
    """ Return data object with the given id.

        Parameters:
            data_id:

        Returns: data object
    """
    return Data.get_by_id(data_id)


def get_all_by_template(template):
    """ Get all data belonging to the specified template.

    Args:
        template:

    Returns:

    """
    return Data.objects(template=template)


def get_all_by_list_template(list_template):
    """ Get all data that belong to the template list.

    Args:
        list_template:

    Returns:

    """
    return Data.get_all_by_list_template(list_template)


def get_all_except(id_list):
    """ Get all data except the ones with the IDs provided.

    Args:
        id_list:

    Returns:

    """
    return Data.get_all_except(id_list)


def execute_query_with_projection(query, projection):
    """ Execute a given query with a projection.

    Args:
        query:
        projection:

    Returns:

    """
    return Data.execute_query(query).only(projection)
