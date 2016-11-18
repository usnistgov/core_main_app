""" XslTransformation API calls
"""
from lxml import etree
from lxml.etree import XMLSyntaxError
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation.models import XslTransformation


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
        xml_dom_tree = etree.XML(xml_data)
        xslt_content = xslt_object.content.encode("utf-8")

        xslt_tree = etree.fromstring(xslt_content)
        xslt_transformation = etree.XSLT(xslt_tree)
    except (UnicodeDecodeError, UnicodeEncodeError):
        raise exceptions.ApiError("An XSLT encoding error happenend while transforming the XML")
    except XMLSyntaxError:
        raise exceptions.ApiError("An XML/XSLT syntax error happenend while transforming the XML")
    except Exception:
        raise exceptions.ApiError("An unexpected exception happened while transforming the XML")

    return str(xslt_transformation(xml_dom_tree))
