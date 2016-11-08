"""
    Xml utils provide tool operation for xml data
"""

from core_main_app.commons.exceptions import XSDError, MDCSError, XMLError

from xml_validation.validation import xerces_validate_xsd, \
    xerces_validate_xml, \
    lxml_validate_xsd, \
    lxml_validate_xml

from lxml import etree
from io import BytesIO
from collections import OrderedDict
import xmltodict
import json

from core_main_app.settings import XERCES_VALIDATION

SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
LXML_SCHEMA_NAMESPACE = "{" + SCHEMA_NAMESPACE + "}"


def validate_xml_schema(xsd_tree):
    """
        Check if XSD schema is valid
        Send XSD Schema to server to be validated
        if XERCES_VALIDATION is true
        :param xsd_tree:
        :return: None if no errors, string otherwise
    """
    if XERCES_VALIDATION:
        try:
            error = xerces_validate_xsd(xsd_tree)
        except Exception:
            error = lxml_validate_xsd(xsd_tree)
    else:
        error = lxml_validate_xsd(xsd_tree)

    return error


def validate_xml_data(xsd_tree, xml_tree):
    """
        Check if XML data is valid
        Send XML data to server to be validated
        if XERCES_VALIDATION is true
        :param xsd_tree:
        :param xml_tree:
        :return: None if no errors, string otherwise
    """
    if XERCES_VALIDATION:
        try:
            error = xerces_validate_xml(xsd_tree, xml_tree)
        except Exception:
            error = lxml_validate_xml(xsd_tree, xml_tree)
    else:
        error = lxml_validate_xml(xsd_tree, xml_tree)

    return error


def is_schema_valid(xsd_string):
    """
        Test if the schema is valid to be uploaded
        :param xsd_string:
        :return:
    """
    if not is_well_formed_xml(xsd_string):
        raise XMLError('Uploaded file is not well formatted XML.')

    # is it supported by the MDCS?
    errors = _get_validity_errors_for_mdcs(xsd_string)
    if len(errors) > 0:
        errors_str = ", ".join(errors)
        raise MDCSError(errors_str)

    error = validate_xml_schema(build_tree(xsd_string))
    if error is not None:
        raise XSDError(error)


def is_well_formed_xml(xml_string):
    """
        True if well formatted XML
        :param xml_string:
        :return:
    """
    # is it a valid XML document?
    try:
        build_tree(xml_string)
    except Exception:
        return False

    return True


def build_tree(xml_string):
    """
        Return a lxml etree from an XML string (xml, xsd...)
        :param xml_string:
        :return:
    """
    try:
        xml_tree = etree.parse(BytesIO(xml_string.encode('utf-8')))
    except Exception:
        xml_tree = etree.parse(BytesIO(xml_string))

    return xml_tree


def unparse(json_dict):
    """
        Unparse JSON data
        :param json_dict:
        :return:
    """
    json_dump_string = json.dumps(json_dict)
    preprocessed_dict = json.loads(json_dump_string,
                                   parse_float=_parse_numbers,
                                   parse_int=_parse_numbers,
                                   object_pairs_hook=OrderedDict)
    return xmltodict.unparse(preprocessed_dict)


def raw_xml_to_dict(raw_xml):
    """
        Transform a raw xml to dict. Returns an empty dict if the parsing failed
        :param raw_xml:
        :return:
        """
    try:
        dict_raw = xmltodict.parse(raw_xml)
    except xmltodict.expat.ExpatError:
        dict_raw = {}

    return dict_raw


def _get_validity_errors_for_mdcs(xsd_string):
    """
        Check that the format of the the schema is supported by the current version of the MDCS
        :param xsd_string:
        :return:
    """
    errors = []

    xsd_tree = build_tree(xsd_string)

    # General Tests

    # get the imports
    imports = xsd_tree.findall("{}import".format(LXML_SCHEMA_NAMESPACE))
    # get the includes
    includes = xsd_tree.findall("{}include".format(LXML_SCHEMA_NAMESPACE))

    if len(imports) != 0 or len(includes) != 0:
        for el_import in imports:
            if 'schemaLocation' not in el_import.attrib:
                errors.append("The attribute schemaLocation of import is required but missing.")
            elif ' ' in el_import.attrib['schemaLocation']:
                errors.append("The use of namespace in import elements is not supported.")
        for el_include in includes:
            if 'schemaLocation' not in el_include.attrib:
                errors.append("The attribute schemaLocation of include is required but missing.")
            elif ' ' in el_include.attrib['schemaLocation']:
                errors.append("The use of namespace in include elements is not supported.")

    # TargetNamespace test
    root = xsd_tree.getroot()
    if 'targetNamespace' in root.attrib:
        target_namespace = root.attrib['targetNamespace']
        if target_namespace not in root.nsmap.values():
            errors.append("The use of a targetNamespace without an associated prefix is not supported.")

    # FIXME: Add tests for Type upload in type api

    return errors


def _parse_numbers(num_str):
    """
    Parse numbers from JSON

    Returns:
        str: parsed string
    """
    return str(num_str)
