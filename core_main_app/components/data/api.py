from .models import Data
from bson.objectid import ObjectId
from core_main_app.commons import exceptions
import core_main_app.components.template.api as template_api
from core_main_app.utils.xml import build_tree, unparse, validate_xml_data

import re
import xmltodict


def get_by_id(data_id):
    """
        Return data object
        :param data_id:
        :return: data object
    """
    try:
        return Data.get_by_id(data_id)
    except:
        raise exceptions.ApiError('No data could be found with the given id')


def get_all():
    """
        List all data
        :return: data collection
    """
    return Data.get_all()


def get_all_by_user(user_id):
    """
        Return all data of a user
        :param user_id:
        :return: data collection
    """
    return Data.get_all_by_user_id(user_id)


def get_all_except_user(user_id):
    """
        Returns all data which are not concern by the user
        :param user_id:
        :return: data collection
    """
    return Data.get_all_except_user_id(user_id)


def get_all_by_id_list(list_ids, distinct_by=None):
    """
        Returns list of XML data from list of ids
        :param list_ids:
        :param distinct_by:
        :return:
    """
    return Data.get_all_by_id_list(list_ids, distinct_by)


def update(data_id, xml_content=None, title=None, user_id=None):
    """
        Change the content of a document
        :param data_id:
        :param xml_content:
        :param title:
        :param user_id:
        :return:
    """

    try:
        data = Data.get_by_id(data_id)

        if xml_content is None:
            content = data.content['content']
        else:
            content = xmltodict.parse(xml_content, postprocessor=_post_processor)

        if title is None:
            title = data.content['title']

        if user_id is None:
            user_id = data.content['user_id']

        json = {'content': content, 'title': title, 'user_id': user_id}

        return Data.update(data_id, json)
    except Exception:
        raise exceptions.ApiError("An error occurred during document's content update.")


def save_with_xml(template_id, title=None, xml=None, user_id=None):
    """
        Save XML data
        :param template_id:
        :param title:
        :param xml:
        :param user_id:
        :return:
    """

    content = None
    if xml is not None:
        _check_xml_data_valid(xml, template_id)
        content = xmltodict.parse(xml, postprocessor=_post_processor)

    if content is not None:
        return Data(template_id=template_id, content=content, title=title, user_id=user_id).save()
    else:
        raise exceptions.ApiError('No data provided. Expected parameter are: xml.')


def save_with_json(template_id, title=None, json=None, user_id=None):
    """
        Save XML data
        :param template_id:
        :param title:
        :param json:
        :param user_id:
        :return:
    """

    content = None
    if json is not None:
        _check_json_data_valid(json, template_id)
        content = json

    if content is not None:
        return Data(template_id=template_id, content=content, title=title, user_id=user_id).save()
    else:
        raise exceptions.ApiError('No data provided. Expected parameter are: json.')


def query(query_value=None, data_id=None, schema_id=None, title=None):
    """
        Execute query on xml data collection
        :param query_value:
        :param data_id:
        :param schema_id:
        :param title:
        :return:
    """
    if query_value is not None:
        return Data.find(query_value)
    else:
        query_value = dict()
        if data_id is not None:
            query_value['_id'] = ObjectId(data_id)
        if schema_id is not None:
            query_value['schema'] = schema_id
        if title is not None:
            if len(title) >= 2 and title[0] == '/' and title[-1] == '/':
                query_value['title'] = re.compile(title[1:-1])
            else:
                query_value['title'] = title
        if len(query_value.keys()) == 0:
            raise exceptions.ApiError("No parameters given.")

        return Data.find(query_value)


def query_full_text(text, template_ids):
    """
        Execute full text query on xml data collection
        :param text:
        :param template_ids:
        :return:
    """
    return Data.execute_full_text_query(text, template_ids)


def _check_xml_data_valid(xml, schema_id):
    """ Check if xml data is valid against a given schema

    :param xml:
    :param schema_id:
    :return:
    """
    template = template_api.get(schema_id)

    try:
        xml_tree = build_tree(xml)
    except:
        raise exceptions.XMLError("Unexpected error: XML is not well formed.")

    try:
        xsd_tree = build_tree(template.content)
    except:
        raise exceptions.XSDError("Unexpected error: XSD is not well formed.")

    error = validate_xml_data(xsd_tree, xml_tree)
    if error is not None:
        raise exceptions.XMLError(error)
    else:
        return None


def _check_json_data_valid(json, schema_id):
    xml_string = unparse(json)
    _check_xml_data_valid(xml_string, schema_id)


def _post_processor(path, key, value):
    """
        Called after XML to JSON transformation
        :param path:
        :param key:
        :param value:
        :return:
    """
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value
