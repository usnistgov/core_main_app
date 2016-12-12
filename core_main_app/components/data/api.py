""" Data API
"""
from core_main_app.components.data.models import Data
from core_main_app.utils.xml import validate_xml_data
from xsd_tree.xsd_tree import XSDTree
import core_main_app.commons.exceptions as exceptions


def get_by_id(data_id):
    """ Return data object with the given id

        Parameters:
            data_id:

        Returns: data object
    """
    return Data.get_by_id(data_id)


def get_all():
    """ List all data

        Returns: data collection
    """
    return Data.get_all()


def get_all_by_user_id(user_id):
    """ Return all data of a user

        Parameters:
            user_id:

        Returns: data collection
    """
    return Data.get_all_by_user_id(user_id)


def get_all_except_user_id(user_id):
    """ Returns all data which are not concern by the user

        Parameters:
             user_id:

        Returns: data collection
    """
    return Data.get_all_except_user_id(user_id)


def get_all_by_id_list(list_ids, distinct_by=None):
    """ Returns list of XML data from list of ids

        Parameters:
            list_ids:
            distinct_by:

        Returns: data collection
    """
    return Data.get_all_by_id_list(list_ids, distinct_by)


def upsert(data):
    """ Save or update the data

    Args:
        data:

    Returns:

    """
    check_xml_file_is_valid(data)
    return data.convert_and_save()


def query_full_text(text, template_ids):
    """ Execute full text query on xml data collection

        Parameters:
            text:
            template_ids:

        Returns:
    """
    return Data.execute_full_text_query(text, template_ids)


def check_xml_file_is_valid(data):
    """ Check if xml data is valid against a given schema

    Args:
        data:

    Returns:

    """
    template = data.template

    try:
        xml_tree = XSDTree.build_tree(data.xml_file)
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




