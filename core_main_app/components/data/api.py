""" Data API
"""
import datetime
from core_main_app.components.data.models import Data
from core_main_app.utils.xml import validate_xml_data
from xml_utils.xsd_tree.xsd_tree import XSDTree
import core_main_app.commons.exceptions as exceptions


def get_by_id(data_id):
    """ Return data object with the given id.

        Parameters:
            data_id:

        Returns: data object
    """
    return Data.get_by_id(data_id)


def get_all():
    """ List all data.

        Returns: data collection
    """
    return Data.get_all()


def get_all_by_user_id(user_id):
    """ Return all data of a user.

        Parameters:
            user_id:

        Returns: data collection
    """
    return Data.get_all_by_user_id(user_id)


def get_all_except_user_id(user_id):
    """ Return all data which are not concern by the user.

        Parameters:
             user_id:

        Returns: data collection
    """
    return Data.get_all_except_user_id(user_id)


def upsert(data):
    """ Save or update the data.

    Args:
        data:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")

    data.last_modification_date = datetime.datetime.now()
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
        raise exceptions.XMLError(e.message)

    try:
        xsd_tree = XSDTree.build_tree(template.content)
    except Exception as e:
        raise exceptions.XSDError(e.message)

    error = validate_xml_data(xsd_tree, xml_tree)
    if error is not None:
        raise exceptions.XMLError(error)
    else:
        return True


def execute_query(query):
    """Execute a query on the Data collection.

    Args:
        query:

    Returns:

    """
    return Data.execute_query(query)


def delete(data):
    """ Delete a data.

    Args:
        data:

    Returns:

    """
    data.delete()


def change_owner(data, new_user):
    """ Change data's owner.

    Args:
        data:
        new_user:

    Returns:
    """
    data.user_id = str(new_user.id)
    data.save()
