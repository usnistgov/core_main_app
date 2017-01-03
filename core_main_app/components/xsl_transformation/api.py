""" XslTransformation API calls
"""
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.utils import xml


def get(xslt_name):
    """ Get an XSLT document

    Returns:
    """
    try:
        return XslTransformation.get_by_name(xslt_name)
    except:
        raise exceptions.ApiError("No transformation can be found with the given name")


def get_all():
    """ Get list of XSLT document

    Returns:
    """
    return XslTransformation.get_all()


def upsert(xsl_transformation):
    """

    Args:
        xsl_transformation:

    Returns:

    """
    return xsl_transformation.save()


def xsl_transform(xml_data, xslt_name):
    """ Transform an XML file using an XSL transformation

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
