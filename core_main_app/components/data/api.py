""" Data API
"""
import datetime

from xml_utils.xsd_tree.xsd_tree import XSDTree

from core_main_app.components.data.models import Data
from core_main_app.utils.xml import validate_xml_data
from core_main_app.commons import exceptions as exceptions
from core_main_app.utils.access_control.decorators import access_control
from core_main_app.components.data.access_control import can_read_data_id, can_read_user, can_write_data, \
    can_read_data_query, can_change_owner


@access_control(can_read_data_id)
def get_by_id(data_id, user):
    """ Return data object with the given id.

        Parameters:
            data_id:
            user:

        Returns: data object
    """
    return Data.get_by_id(data_id)


@access_control(can_read_user)
def get_all(user):
    """ Return all data accessible by a user.

        Parameters:
            user:

        Returns: data collection
    """
    return Data.get_all_by_user_id(str(user.id))


@access_control(can_read_user)
def get_all_except_user(user):
    """ Return all data which are not created by the user.

        Parameters:
             user:

        Returns: data collection
    """
    return Data.get_all_except_user_id(str(user.id))


@access_control(can_write_data)
def upsert(data, user):
    """ Save or update the data.

    Args:
        data:
        user:

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


@access_control(can_read_data_query)
def execute_query(query, user):
    """Execute a query on the Data collection.

    Args:
        query:
        user:

    Returns:

    """
    return Data.execute_query(query)


@access_control(can_write_data)
def delete(data, user):
    """ Delete a data.

    Args:
        data:
        user:

    Returns:

    """
    data.delete()


@access_control(can_change_owner)
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
