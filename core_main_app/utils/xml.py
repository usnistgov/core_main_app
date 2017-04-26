"""
    Xml utils provide too l operation for xml data
"""
from django.core.urlresolvers import reverse
import core_main_app.commons.exceptions as exceptions
import xml_utils.xml_validation.validation as xml_validation
from xml_utils.xsd_tree.xsd_tree import XSDTree
import xml_utils.commons.constants as xml_utils_constants
from lxml import etree
from collections import OrderedDict
import xmltodict
import json
from xml_utils.xsd_hash import xsd_hash

from core_main_app.settings import XERCES_VALIDATION, SERVER_URI


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

    error = validate_xml_schema(XSDTree.build_tree(xsd_string))
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
        XSDTree.build_tree(xml_string)
    except Exception:
        return False

    return True


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
        updated_xsd_string = XSDTree.tostring(xsd_tree)
    else:
        raise exceptions.XSDError(error.replace("'", ""))

    return updated_xsd_string


def get_hash(xml_string):
    """
    Get the hash of an XML string
    :param xml_string:
    :return:
    """
    try:
        return xsd_hash.get_hash(xml_string)
    except Exception, e:
        raise exceptions.XSDError("Something wrong happened during the hashing.")


def post_processor(path, key, value):
    """ Called after XML to JSON transformation

        Parameters:
            path:
            key:
            value:

        Returns:
    """
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value


def get_imports_and_includes(xsd_string):
    """
    Get a list of imports and includes in the file
    :param xsd_string:
    :return: list of imports, list of includes
    """
    xsd_tree = XSDTree.build_tree(xsd_string)
    # get the imports
    imports = xsd_tree.findall("{}import".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))
    # get the includes
    includes = xsd_tree.findall("{}include".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))
    return imports, includes


def update_dependencies(xsd_string, dependencies):
    """
    Update dependencies of the schemas with given dependencies
    :param xsd_string:
    :param dependencies:
    :return:
    """
    # build the tree
    xsd_tree = XSDTree.build_tree(xsd_string)
    # get the imports
    xsd_imports = xsd_tree.findall("{}import".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))
    # get the includes
    xsd_includes = xsd_tree.findall("{}include".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))

    for schema_location, dependency_id in dependencies.iteritems():
        if dependency_id is not None:
            for xsd_include in xsd_includes:
                if schema_location == xsd_include.attrib['schemaLocation']:
                    xsd_include.attrib['schemaLocation'] = _get_schema_location_uri(dependency_id)

            for xsd_import in xsd_imports:
                if schema_location == xsd_import.attrib['schemaLocation']:
                    xsd_import.attrib['schemaLocation'] = _get_schema_location_uri(dependency_id)
    return xsd_tree


def _check_core_support(xsd_string):
    """Checks that the format of the the schema is supported by the current version of the Core

    Args:
        xsd_string:

    Returns:

    """
    # list of errors
    errors = []

    # build xsd tree
    xsd_tree = XSDTree.build_tree(xsd_string)

    # get the imports
    imports = xsd_tree.findall("{}import".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))
    # get the includes
    includes = xsd_tree.findall("{}include".format(xml_utils_constants.LXML_SCHEMA_NAMESPACE))

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

    return errors


def _parse_numbers(num_str):
    """
    Parse numbers from JSON

    Returns:
        str: parsed string
    """
    return str(num_str)


def _get_schema_location_uri(schema_id):
    """
    Get an URI of the schema location on the system from an id
    :param schema_id:
    :return:
    """
    url = reverse('core_main_app_rest_template_download')
    return str(SERVER_URI) + url + '?id=' + str(schema_id)


def xsl_transform(xml_string, xslt_string):
    """

    Args:
        xml_string:
        xslt_string:

    Returns:

    """
    try:
        # Build the XSD and XSLT tree
        xslt_tree = XSDTree.build_tree(xslt_string)
        xsd_tree = XSDTree.build_tree(xml_string)

        # Get the XSLT transformation and transform the XSD
        transform = etree.XSLT(xslt_tree)
        transformed_tree = transform(xsd_tree)
        return str(transformed_tree)
    except Exception:
        raise exceptions.CoreError("An unexpected exception happened while transforming the XML")

