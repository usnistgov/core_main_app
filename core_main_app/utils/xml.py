"""
    Xml utils provide tool operation for xml data
"""
import core_main_app.commons.exceptions as exceptions
import xml_validation.validation as xml_validation
from lxml import etree
from io import BytesIO
from collections import OrderedDict
import xmltodict
import json

from core_main_app.settings import XERCES_VALIDATION, SERVER_URI

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
            error = xml_validation.xerces_validate_xsd(xsd_tree)
        except Exception:
            error = xml_validation.lxml_validate_xsd(xsd_tree)
    else:
        error = xml_validation.lxml_validate_xsd(xsd_tree)

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
            error = xml_validation.xerces_validate_xml(xsd_tree, xml_tree)
        except Exception:
            error = xml_validation.lxml_validate_xml(xsd_tree, xml_tree)
    else:
        error = xml_validation.lxml_validate_xml(xsd_tree, xml_tree)

    return error


def is_schema_valid(xsd_string):
    """
        Test if the schema is valid to be uploaded
        :param xsd_string:
        :return:
    """
    if not is_well_formed_xml(xsd_string):
        raise exceptions.XMLError('Uploaded file is not well formatted XML.')

    # Check schema support by the core
    errors = _check_core_support(xsd_string)
    if len(errors) > 0:
        errors_str = ", ".join(errors)
        raise exceptions.CoreError(errors_str)

    error = validate_xml_schema(build_tree(xsd_string))
    if error is not None:
        raise exceptions.XSDError(error)


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


def raw_xml_to_dict(raw_xml, postprocessor=None):
    """
        Transform a raw xml to dict. Returns an empty dict if the parsing failed
        :param raw_xml:
        :param postprocessor:
        :return:
        """
    try:
        dict_raw = xmltodict.parse(raw_xml, postprocessor=postprocessor)
        return dict_raw
    except xmltodict.expat.ExpatError:
        raise exceptions.XMLError("An unexpected error happened during the XML parsing.")


def _check_core_support(xsd_string):
    """
        Check that the format of the the schema is supported by the current version of the Core
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


def tree_to_string(xml_tree, pretty=False):
    """
    Return an XML String from a lxml etree
    :param xml_tree:
    :param pretty: True for indented print
    :return:
    """
    try:
        xml_tree = etree.tostring(xml_tree, pretty_print=pretty)
    except Exception:
        raise exceptions.XMLError("Something went wrong during conversion of the tree to a string.")

    return xml_tree


def get_imports_and_includes(xsd_string):
    """
    Get a list of imports and includes in the file
    :param xsd_string:
    :return: list of imports, list of includes
    """
    xsd_tree = build_tree(xsd_string)
    # get the imports
    imports = xsd_tree.findall("{}import".format(LXML_SCHEMA_NAMESPACE))
    # get the includes
    includes = xsd_tree.findall("{}include".format(LXML_SCHEMA_NAMESPACE))
    return imports, includes


def update_dependencies(xsd_string, dependencies):
    """
    Update dependencies of the schemas with given dependencies
    :param xsd_string:
    :param dependencies:
    :return:
    """
    # build the tree
    xsd_tree = build_tree(xsd_string)
    # get the imports
    xsd_imports = xsd_tree.findall("{}import".format(LXML_SCHEMA_NAMESPACE))
    # get the includes
    xsd_includes = xsd_tree.findall("{}include".format(LXML_SCHEMA_NAMESPACE))

    for schema_location, dependency_id in dependencies.iteritems():
        if dependency_id is not None:
            for xsd_include in xsd_includes:
                if schema_location == xsd_include.attrib['schemaLocation']:
                    xsd_include.attrib['schemaLocation'] = _get_schema_location_uri(dependency_id)

            for xsd_import in xsd_imports:
                if schema_location == xsd_import.attrib['schemaLocation']:
                    xsd_import.attrib['schemaLocation'] = _get_schema_location_uri(dependency_id)
    return xsd_tree


def _get_schema_location_uri(schema_id):
    """
    Get an URI of the schema location on the system from an id
    :param schema_id:
    :return:
    """
    return str(SERVER_URI)+'/rest/types/get-dependency?id=' + str(schema_id)


def get_template_with_server_dependencies(xsd_string, dependencies):
    """
    Return the template with schema locations pointing to the server
    :param xsd_string:
    :param dependencies:
    :return:
    """
    # replace includes/imports by API calls (get dependencies starting by the imports)
    try:
        xsd_tree = update_dependencies(xsd_string, dependencies)
    except Exception, e:
        raise exceptions.XSDError("Something went wrong during dependency update.")

    # validate the schema
    try:
        error = validate_xml_schema(xsd_tree)
    except Exception, e:
        raise exceptions.XSDError("Something went wrong during XSD validation.")

    # is it a valid XML document ?
    if error is None:
        try:
            updated_xsd_string = tree_to_string(xsd_tree)
        except Exception, e:
            raise exceptions.XSDError("An unexpected error happened during dependency update.")
    else:
        raise exceptions.XSDError(error.replace("'", ""))

    return updated_xsd_string
