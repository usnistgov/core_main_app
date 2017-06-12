""" XslTransformation API calls
"""
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils import xml
from core_main_app.utils.xml import is_well_formed_xml


def get(xslt_name):
    """ Get an XSLT document.

    Returns:
    """
    try:
        return XslTransformation.get_by_name(xslt_name)
    except:
        raise exceptions.ApiError("No transformation can be found with the given name")


def get_by_id(xslt_id):
    """ Get an XSLT document by its id.

    Args:
        xslt_id: Id.

    Returns:
        XslTransformation object.

    """
    return XslTransformation.get_by_id(xslt_id)


def get_all():
    """ Get list of XSLT document.

    Returns:
    """
    return XslTransformation.get_all()


# TODO: Add namespace check
def upsert(xsl_transformation):
    """ Upsert an xsl_transformation.

    Args:
        xsl_transformation: XslTransformation.

    Returns:
        XslTransformation instance.

    """
    is_well_formed = is_well_formed_xml(xsl_transformation.content)
    if is_well_formed:
        return xsl_transformation.save_object()
    else:
        raise exceptions.ApiError("Uploaded file is not well formatted XSLT.")


def delete(xsl_transformation):
    """ Delete an xsl_transformation.

    Args:
        xsl_transformation: XslTransformation to delete.

    """
    xsl_transformation.delete()


def xsl_transform(xml_data, xslt_name):
    """ Transform an XML file using an XSL transformation.

    Args:
        xml_data (str): XML document content, encoded in UTF-8
        xslt_name (str): Name of an XslTransformation document

    Returns:
        str: Transformed XML string
    """
    xslt_object = get(xslt_name)

    try:
        return xml.xsl_transform(xml_data, xslt_object.content)
    except Exception:
        raise exceptions.ApiError("An unexpected exception happened while transforming the XML")
