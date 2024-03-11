""" Xml utils for the core applications
"""
import logging
import re
from urllib.parse import urlparse

import xmltodict
from django.urls import reverse

from core_main_app.commons import exceptions
from core_main_app.settings import XERCES_VALIDATION, SERVER_URI
from core_main_app.utils.resolvers.resolver_utils import lmxl_uri_resolver
from core_main_app.utils.urls import get_template_download_pattern
from xml_utils import xpath as xml_utils_xpath
from xml_utils.commons import constants as xml_utils_constants
from xml_utils.commons import exceptions as xml_utils_exceptions
from xml_utils.commons.constants import XSL_NAMESPACE
from xml_utils.xml_validation import validation as xml_validation
from xml_utils.xsd_hash import xsd_hash
from xml_utils.xsd_tree.operations.namespaces import get_namespaces
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


def validate_xml_schema(xsd_tree, *args, **kwargs):
    """Check if XSD schema is valid, send XSD Schema to server to be validated if
    XERCES_VALIDATION is true.

    Args:
        xsd_tree:

    Returns: None if no errors, string otherwise

    """
    if XERCES_VALIDATION:
        try:
            error = xml_validation.xerces_validate_xsd(xsd_tree)
        except Exception:
            error = xml_validation.lxml_validate_xsd(
                xsd_tree, lmxl_uri_resolver(*args, **kwargs)
            )
    else:
        error = xml_validation.lxml_validate_xsd(
            xsd_tree, lmxl_uri_resolver(*args, **kwargs)
        )

    return error


def validate_xml_data(xsd_tree, xml_tree, *args, **kwargs):
    """Check if XML data is valid, send XML data to server to be validated if XERCES_VALIDATION is true

    Args:
        xsd_tree:
        xml_tree:

    Returns:None if no errors, string otherwise

    """
    if XERCES_VALIDATION:
        try:
            error = xml_validation.xerces_validate_xml(xsd_tree, xml_tree)
        except Exception:
            error = xml_validation.lxml_validate_xml(
                xsd_tree, xml_tree, lmxl_uri_resolver(*args, **kwargs)
            )
    else:
        error = xml_validation.lxml_validate_xml(
            xsd_tree, xml_tree, lmxl_uri_resolver(*args, **kwargs)
        )

    return error


def is_schema_valid(xsd_string, *args, **kwargs):
    """Test if the schema is valid to be uploaded.

    Args:
        xsd_string:

    Returns:

    """
    if not is_well_formed_xml(xsd_string):
        raise exceptions.XMLError("Uploaded file is not well formatted XML.")

    # Check schema support by the core
    errors = _check_core_support(xsd_string)
    if len(errors) > 0:
        errors_str = ", ".join(errors)
        raise exceptions.CoreError(errors_str)

    error = validate_xml_schema(
        XSDTree.build_tree(xsd_string), *args, **kwargs
    )
    if error is not None:
        raise exceptions.XSDError(error)


def is_well_formed_xml(xml_string):
    """True if well formatted XML.

    Args:
        xml_string:

    Returns:

    """
    # is it a valid XML document?
    try:
        XSDTree.build_tree(xml_string)
    except Exception:
        return False

    return True


def format_content_xml(xml_string):
    """Format XML content.

    Args:
        xml_string:

    Returns:

    """

    try:
        xml_tree = XSDTree.build_tree(xml_string)
        return XSDTree.tostring(xml_tree, pretty=True)
    except Exception:
        raise exceptions.XMLError("Content is not well formatted XML.")


def has_xsl_namespace(xml_string):
    """True if XML has the XSL namespace.

    Args:
        xml_string:

    Returns:

    """
    has_namespace = False
    try:
        has_namespace = XSL_NAMESPACE in list(
            get_namespaces(xml_string).values()
        )
    except Exception as exception:
        logger.warning(
            "has_xsl_namespace threw an exception: %s", str(exception)
        )

    return has_namespace


def raw_xml_to_dict(
    raw_xml, postprocessor=None, force_list=None, list_limit=None
):
    """Transform a raw xml to dict. Returns an empty dict if the parsing failed.

    Args:
        raw_xml:
        postprocessor:
        force_list:
        list_limit:

    Returns:

    """
    try:
        if postprocessor:
            # set postprocessor function if found in the list (XML_POST_PROCESSORS)
            postprocessor = (
                XML_POST_PROCESSORS[postprocessor]
                if postprocessor in XML_POST_PROCESSORS
                else postprocessor
            )
            # check if postprocessor is callable
            if not callable(postprocessor):
                raise exceptions.CoreError("postprocessor is not callable")

        # convert xml to dict
        dict_raw = xmltodict.parse(
            raw_xml, postprocessor=postprocessor, force_list=force_list
        )
        if list_limit:
            # Remove lists which size exceed the limit size
            remove_lists_from_xml_dict(dict_raw, list_limit)
        return dict_raw
    except xmltodict.expat.ExpatError:
        raise exceptions.XMLError(
            "An unexpected error happened during the XML parsing."
        )


def remove_lists_from_xml_dict(xml_dict, max_list_size=0):
    """Remove from dictionary the lists that exceed max list size.

    Args:
        xml_dict:
        max_list_size:

    Returns:

    """
    # init list of keys to delete
    keys_to_delete = []
    # iterate key, values
    for key, value in xml_dict.items():
        # if value is a list
        if isinstance(value, list):
            # if list's size is higher than maximum size
            if len(value) > max_list_size:
                # mark key for deletion
                keys_to_delete.append(key)
        # if value is a dict
        elif isinstance(value, dict):
            # continue recursion on value
            remove_lists_from_xml_dict(value, max_list_size)
    # delete keys marked for deletion
    for key_to_delete in keys_to_delete:
        del xml_dict[key_to_delete]


def get_template_with_server_dependencies(
    xsd_string, dependencies, request=None
):
    """Return the template with schema locations pointing to the server.

    Args:
        xsd_string:
        dependencies:
        request:

    Returns:

    """
    # replace includes/imports by API calls (get dependencies starting by the imports)
    try:
        xsd_tree = update_dependencies(xsd_string, dependencies)
    except Exception:
        raise exceptions.XSDError(
            "Something went wrong during dependency update."
        )

    # validate the schema
    try:
        error = validate_xml_schema(xsd_tree, request=request)
    except Exception:
        raise exceptions.XSDError(
            "Something went wrong during XSD validation."
        )

    # is it a valid XML document ?
    if error is None:
        updated_xsd_string = XSDTree.tostring(xsd_tree)
    else:
        raise exceptions.XSDError(error.replace("'", ""))

    return updated_xsd_string


def get_hash(xml_string):
    """Get the hash of an XML string.

    Args:
        xml_string:

    Returns:

    """
    try:
        return xsd_hash.get_hash(xml_string)
    except Exception:
        raise exceptions.XSDError(
            "Something wrong happened during the hashing."
        )


def get_numeric_value(value):
    """Convert the value to the true type

    abc -> "abc"
    1 -> 1
    1.0 -> 1.0

    Args:
        value:

    Returns:

    """
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            return value


def get_string_and_numeric_values(value):
    """Get string and numeric values

    abc -> "abc"
    1 -> ("1", 1)
    1.0 -> ("1.0", 1.0)

    Args:
        value:

    Returns:

    """
    try:
        return value, int(value)
    except (ValueError, TypeError):
        try:
            return value, float(value)
        except (ValueError, TypeError):
            return value


def numeric_post_processor(path, key, value):
    """Convert to numeric values"""
    return key, get_numeric_value(value)


def numeric_and_string_post_processor(path, key, value):
    """Convert to string and numeric values"""
    return key, get_string_and_numeric_values(value)


XML_POST_PROCESSORS = {
    "NUMERIC": numeric_post_processor,
    "NUMERIC_AND_STRING": numeric_and_string_post_processor,
}


def get_imports_and_includes(xsd_string):
    """Get a list of imports and includes in the file.

    Args:
        xsd_string:

    Returns: list of imports, list of includes

    """
    xsd_tree = XSDTree.build_tree(xsd_string)
    # get the imports
    imports = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}import"
    )
    # get the includes
    includes = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}include"
    )
    return imports, includes


def update_dependencies(xsd_string, dependencies):
    """Update dependencies of the schemas with given dependencies.

    Args:
        xsd_string:
        dependencies:

    Returns:

    """
    # build the tree
    xsd_tree = XSDTree.build_tree(xsd_string)
    # get the imports
    xsd_imports = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}import"
    )
    # get the includes
    xsd_includes = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}include"
    )

    for schema_location, dependency_id in dependencies.items():
        if dependency_id is not None:
            for xsd_include in xsd_includes:
                if schema_location == xsd_include.attrib["schemaLocation"]:
                    xsd_include.attrib[
                        "schemaLocation"
                    ] = _get_schema_location_uri(dependency_id)

            for xsd_import in xsd_imports:
                if schema_location == xsd_import.attrib["schemaLocation"]:
                    xsd_import.attrib[
                        "schemaLocation"
                    ] = _get_schema_location_uri(dependency_id)
    return xsd_tree


def get_local_dependencies(xsd_string):
    """Get local dependencies from an xsd.

    Args:
        xsd_string: XSD as string.

    Returns:
        Local dependencies

    """
    # declare list of dependencies
    dependencies = []
    # Get includes and imports
    imports, includes = get_imports_and_includes(xsd_string)
    # list of includes and imports
    xsd_includes_imports = imports + includes

    # get pattern to match the url to download a template
    pattern = get_template_download_pattern()

    for xsd_include_import in xsd_includes_imports:
        if xsd_include_import.attrib["schemaLocation"].startswith(SERVER_URI):
            try:
                # parse dependency url
                url = urlparse(xsd_include_import.attrib["schemaLocation"])
                # get id from url
                object_id = pattern.match(url.path).group("pk")
                # add id to list of internal dependencies
                dependencies.append(object_id)
            except Exception:
                raise exceptions.XMLError(
                    "Local dependency schemaLocation is not well formed."
                )

    return dependencies


def _check_core_support(xsd_string):
    """Check that the format of the the schema is supported by the current version of the Core.

    Args:
        xsd_string:

    Returns:

    """
    # list of errors
    errors = []

    # build xsd tree
    xsd_tree = XSDTree.build_tree(xsd_string)

    # get the imports
    imports = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}import"
    )
    # get the includes
    includes = xsd_tree.findall(
        f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}include"
    )

    if len(imports) != 0 or len(includes) != 0:
        for el_import in imports:
            if "schemaLocation" not in el_import.attrib:
                errors.append(
                    "The attribute schemaLocation of import is required but missing."
                )
            elif " " in el_import.attrib["schemaLocation"]:
                errors.append(
                    "The use of namespace in import elements is not supported."
                )
        for el_include in includes:
            if "schemaLocation" not in el_include.attrib:
                errors.append(
                    "The attribute schemaLocation of include is required but missing."
                )
            elif " " in el_include.attrib["schemaLocation"]:
                errors.append(
                    "The use of namespace in include elements is not supported."
                )

    return errors


def _parse_numbers(num_str):
    """Parse numbers from JSON.

    Returns:
        str: parsed string
    """
    return str(num_str)


def _get_schema_location_uri(schema_id):
    """Get an URI of the schema location on the system from an id.

    Args:
        schema_id:

    Returns:

    """
    url = reverse(
        "core_main_app_rest_template_download", kwargs={"pk": str(schema_id)}
    )
    return str(SERVER_URI) + url


def xsl_transform(xml_string, xslt_string):
    """Apply transformation to xml.

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
        transform = XSDTree.transform_to_xslt(xslt_tree)
        transformed_tree = transform(xsd_tree)
        return str(transformed_tree)
    except Exception:
        raise exceptions.CoreError(
            "An unexpected exception happened while transforming the XML"
        )


def xpath_to_dot_notation(xpath, namespaces=None):
    """Transforms XML xpath into dot notation

    Args:
        xpath:
        namespaces:

    Returns:

    """
    if namespaces is None:
        namespaces = {"xml": xml_utils_constants.XML_NAMESPACE}

    # remove indexes from xpath
    xpath = re.sub(r"\[[0-9]+\]", "", xpath)
    # remove namespaces
    for prefix in list(namespaces.keys()):
        xpath = re.sub(r"{}:".format(prefix), "", xpath)
    # replace / by .
    xpath = xpath.replace("/", ".")

    # Return xpath without first .
    return xpath[1:] if xpath[0] == "." else xpath


def validate_xpath(xpath):
    """Validate a provided xpath.

    Args:
        xpath:

    Raises:
        core_main_app.commons.exceptions.CoreError
    """
    try:
        xml_utils_xpath.validate_xpath(xpath)
    except xml_utils_exceptions.XPathError as exception:
        raise exceptions.XMLError(str(exception))


def get_content_by_xpath(xml_string, xpath, namespaces=None):
    """Get list of xml content by xpath

    Args:
        xml_string:
        xpath:
        namespaces:

    Returns:

    """
    # Build lxml tree from xml string
    xsd_tree = XSDTree.build_tree(xml_string)
    # Get values at xpath
    values_list = xsd_tree.xpath(xpath, namespaces=namespaces)

    # Build list of string values
    str_values_list = list()
    # Iterate through all xml elements found
    for value in values_list:
        # Get string value for element
        str_value = (
            value if isinstance(value, str) else XSDTree.tostring(value)
        )
        # Add value to list
        str_values_list.append(str_value)

    # Return list of string values found at xpath
    return str_values_list
