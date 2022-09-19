""" XslTransformation API calls
"""
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils import xml
from core_main_app.utils.xml import is_well_formed_xml, has_xsl_namespace


def get_by_name(xslt_name):
    """Get an XSLT document.

    Returns:
    """
    try:
        return XslTransformation.get_by_name(xslt_name)
    except Exception:
        raise exceptions.ApiError(
            "No transformation can be found with the given name"
        )


def get_by_id(xslt_id):
    """Get an XSLT document by its id.

    Args:
        xslt_id: Id.

    Returns:
        XslTransformation object.

    """
    return XslTransformation.get_by_id(xslt_id)


def get_all():
    """Get list of XSLT document.

    Returns:
    """
    return XslTransformation.get_all()


def upsert(xsl_transformation):
    """Upsert an xsl_transformation.

    Args:
        xsl_transformation: XslTransformation.

    Returns:
        XslTransformation instance.

    """
    if not is_well_formed_xml(xsl_transformation.content):
        raise exceptions.ApiError("Uploaded file is not well formatted XSLT.")
    elif not has_xsl_namespace(xsl_transformation.content):
        raise exceptions.ApiError(
            "XSLT namespace not found in the uploaded file."
        )
    else:
        xsl_transformation.save_object()
        return xsl_transformation


def delete(xsl_transformation):
    """Delete an xsl_transformation.

    Args:
        xsl_transformation: XslTransformation to delete.

    """
    xsl_transformation.delete()


def xsl_transform(xml_content, xslt_name):
    """Transform an XML file using an XSL transformation.

    Args:
        xml_content (str): XML document content, encoded in UTF-8
        xslt_name (str): Name of an XslTransformation document

    Returns:
        str: Transformed XML string
    """
    xslt_object = get_by_name(xslt_name)

    try:
        return xml.xsl_transform(xml_content, xslt_object.content)
    except Exception:
        raise exceptions.ApiError(
            "An unexpected exception happened while transforming the XML"
        )


def get_by_id_list(list_data_id):
    """Return a list of xsl_transformation object with the given list id.

    Parameters:
        list_data_id:

    Returns: data object
    """
    return XslTransformation.get_by_id_list(list_data_id)


def get_none():
    """Return None object

    Returns:

    """
    return XslTransformation.objects.none()
