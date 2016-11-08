""" XslTransformation API calls
"""
from lxml import etree
from lxml.etree import XMLSyntaxError
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation.models import XslTransformation


def get(xslt_name):
    """ Get an XSLT document

    :return:
    """
    try:
        return XslTransformation.get_by_name(xslt_name)
    except:
        raise exceptions.ApiError("No transformation can be found with the given name")


def get_all():
    """ Get list of XSLT document

    :return:
    """
    return XslTransformation.get_all()


def update(xslt_name, xslt_filename=None, xslt_content=None):
    """ Create an XSLT document

    Parameters:
        xslt_name (str):
        xslt_filename (str):
        xslt_content (str):

    Returns:
    """
    xslt_object = get(xslt_name)

    if xslt_filename is not None:
        xslt_object.filename = xslt_filename

    if xslt_content is not None:
        xslt_object.content = xslt_content

    return xslt_object.save()


def create(xslt_name, xslt_filename, xslt_content):
    """ Create an XSLT document

    Parameters:
        xslt_name (str):
        xslt_filename (str):
        xslt_content (str):

    Returns:
    """
    return XslTransformation(
        name=xslt_name,
        filename=xslt_filename,
        content=xslt_content
    ).save()


def xsl_transform(xml_data, xslt_name):
    """ Transform an XML file using an XSL transformation

    Parameters:
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
