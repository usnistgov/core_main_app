"""
    Xml utils provide too l operation for xml data
"""
from django.core.urlresolvers import reverse
import core_main_app.commons.exceptions as exceptions
import xml_utils.xml_validation.validation as xml_validation
from xml_utils.xsd_tree.xsd_tree import XSDTree
import xml_utils.commons.constants as xml_utils_constants
from lxml import etree
from io import BytesIO
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
        try:
            updated_xsd_string = tree_to_string(xsd_tree)
        except Exception, e:
            raise exceptions.XSDError("An unexpected error happened during dependency update.")
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
    """
        Check that the format of the the schema is supported by the current version of the Core
        :param xsd_string:
        :return:
    """
    errors = []

    xsd_tree = XSDTree.build_tree(xsd_string)

    # General Tests

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


def _get_schema_location_uri(schema_id):
    """
    Get an URI of the schema location on the system from an id
    :param schema_id:
    :return:
    """
    url = reverse('core_main_app_rest_template_download')
    return str(SERVER_URI) + url + '?id=' + str(schema_id)


def get_namespaces(xsd_string):
    """Returns dict of prefix and namespaces

    Args:
        xsd_string:

    Returns:

    """
    xsd_file = BytesIO(str(xsd_string))
    events = "start", "start-ns"
    ns = {'xml': xml_utils_constants.XML_NAMESPACE}
    for event, elem in etree.iterparse(xsd_file, events):
        if event == "start-ns":
            if len(elem[0]) > 0 and len(elem[1]) > 0:
                ns[elem[0]] = "%s" % elem[1]
        elif event == "start":
            break

    return ns


def get_default_prefix(namespaces):
    """Returns the default prefix used in the schema

    Args:
        namespaces:

    Returns:

    """
    default_prefix = ''
    for prefix, url in namespaces.items():
        if url == xml_utils_constants.SCHEMA_NAMESPACE:
            default_prefix = prefix
            break

    return default_prefix


def get_element_by_xpath(xsd_tree, xpath, namespaces=None):
    """Returns an element from its xpath

    Args:
        xsd_tree:
        xpath:
        namespaces:

    Returns:

    """
    if namespaces is not None:
        # Get default prefix
        default_prefix = get_default_prefix(namespaces)

        # Transform xpath into LXML format
        xpath = xpath.replace(default_prefix + ":", xml_utils_constants.LXML_SCHEMA_NAMESPACE)

    try:
        element = xsd_tree.find(xpath)
    except:
        raise exceptions.XSDError('Unable to find an element for the given Xpath.')

    if element is not None:
        return element
    else:
        raise exceptions.XSDError('Unable to find an element for the given Xpath.')


def set_attribute(xsd_string, xpath, attribute, value):
    """Sets an attribute of an element

    Args:
        xsd_string:
        xpath:
        attribute:
        value:

    Returns:

    """
    return _update_attribute(xsd_string, xpath, attribute, value)


def delete_attribute(xsd_string, xpath, attribute):
    """Delete an attribute from an element

    Args:
        xsd_string:
        xpath:
        attribute:

    Returns:

    """
    return _update_attribute(xsd_string, xpath, attribute)


def _update_attribute(xsd_string, xpath, attribute, value=None):
    """

    Args:
        xsd_string:
        xpath: xpath of the element to update
        attribute: name of the attribute to update
        value: value of the attribute to set

    Returns:

    """
    # Build the XSD tree
    xsd_tree = XSDTree.build_tree(xsd_string)
    # Get namespaces
    namespaces = get_namespaces(xsd_string)
    # Get XSD element using its xpath
    element = get_element_by_xpath(xsd_tree, xpath, namespaces)

    # Add or update the attribute
    if value is not None:
        # Set element attribute with value
        element.attrib[attribute] = value
    else:
        # Deletes attribute
        if attribute in element.attrib:
            del element.attrib[attribute]

    # Converts XSD tree back to string
    updated_xsd_string = tree_to_string(xsd_tree)

    return updated_xsd_string


def xsl_transform(xml_string, xslt_string):
    """

    Args:
        xml_string:
        xslt_string:

    Returns:

    """
    # Build the XSLT tree
    xslt_tree = XSDTree.build_tree(xslt_string)
    # Get the transform
    transform = etree.XSLT(xslt_tree)
    # Build the XML tree
    xsd_tree = XSDTree.build_tree(xml_string)
    # Get the transformed tree
    transformed_tree = transform(xsd_tree)
    return str(transformed_tree)


def add_appinfo_element(xsd_string, xpath, appinfo_name, value):
    """Adds appinfo to an element

    Args:
        xsd_string:
        xpath:
        appinfo_name:
        value:

    Returns:

    """
    return _update_appinfo_element(xsd_string, xpath, appinfo_name, value)


def delete_appinfo_element(xsd_string, xpath, attribute_name):
    """Deletes appinfo from an element

    Args:
        xsd_string:
        xpath:
        attribute_name:

    Returns:

    """
    return _update_appinfo_element(xsd_string, xpath, attribute_name)


def _get_or_create_element(parent, element_tag, namespace=""):
    """Gets an element in children or creates it

    Args:
        parent:
        element_tag:
        namespace:

    Returns:

    """
    element = parent.find("./{0}{1}".format(namespace, element_tag))
    if element is None:
        # create element if absent
        element = etree.Element("{0}{1}".format(namespace, element_tag))
        # insert element
        parent.insert(0, element)

    return element


def _get_appinfo_element(element, element_name, namespace):
    """Get an element from the appinfo

    Args:
        element:
        element_name:
        namespace:

    Returns:

    """
    appinfo_elements = element.findall("./{0}annotation/{0}appinfo/{1}".format(namespace, element_name))

    if len(appinfo_elements) == 1:
        return appinfo_elements[0]
    elif len(appinfo_elements) > 1:
        raise exceptions.XSDError("{} appinfo found multiple times in the same element".format(element_name))
    elif len(appinfo_elements) == 0:
        return None


def _update_appinfo_element(xsd_string, xpath, appinfo_name, value=None):
    """Updates an appinfo element

    Args:
        xsd_string:
        xpath: xpath to element to update
        attribute_name: name of the attribute to update
        value: value to set

    Returns:

    """
    # Build the XSD tree
    xsd_tree = XSDTree.build_tree(xsd_string)
    # Get namespaces
    namespaces = get_namespaces(xsd_string)
    # Get XSD element using its xpath
    element = get_element_by_xpath(xsd_tree, xpath, namespaces)

    if value is not None:
        # If a value is provided, create or update the appinfo
        add_appinfo_child_to_element(element, appinfo_name, value)
    else:
        # value is None, deletes the appinfo if present
        delete_appinfo_child_from_element(element, appinfo_name)

    # Converts XSD tree back to string
    updated_xsd_string = tree_to_string(xsd_tree)

    return updated_xsd_string


def add_appinfo_child_to_element(element, appinfo_name, value):
    """Adds ab appinfo child to an etree element

    Args:
        element:
        appinfo_name:
        value:

    Returns:

    """
    # Get the appinfo element
    appinfo_element = _get_appinfo_element(element, appinfo_name, xml_utils_constants.LXML_SCHEMA_NAMESPACE)

    # if appinfo is absent, creates it
    if appinfo_element is None:
        # get annotation tag
        annotation = _get_or_create_element(element, "annotation", xml_utils_constants.LXML_SCHEMA_NAMESPACE)

        # get appinfo tag
        appinfo = _get_or_create_element(annotation, "appinfo", xml_utils_constants.LXML_SCHEMA_NAMESPACE)

        # get attribute tag
        appinfo_element = _get_or_create_element(appinfo, appinfo_name)

    # set the value of the appinfo
    appinfo_element.text = value


def delete_appinfo_child_from_element(element, appinfo_name):
    """Deletes an appinfo child an etree element

    Args:
        element:
        appinfo_name: name of the appinfo to delete

    Returns:

    """
    # Get the appinfo element
    appinfo_element = _get_appinfo_element(element, appinfo_name, xml_utils_constants.LXML_SCHEMA_NAMESPACE)

    # if appinfo is present, deletes it
    if appinfo_element is not None:
        appinfo_element.getparent().remove(appinfo_element)
