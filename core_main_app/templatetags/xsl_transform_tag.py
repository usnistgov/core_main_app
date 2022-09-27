"""XSL Transformation tag
"""

from django import template
from django.contrib.staticfiles import finders

from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.xsl_transformation import (
    api as xsl_transformation_api,
)
from core_main_app.settings import DEFAULT_DATA_RENDERING_XSLT
from core_main_app.utils.file import read_file_content
from core_main_app.utils.xml import xsl_transform

register = template.Library()


class XSLType:
    """XSLType"""

    type_list = "List"
    type_detail = "Detail"


@register.simple_tag(name="xsl_transform_list")
def render_xml_as_html_list(*args, **kwargs):
    """Render an XML to HTML using the list xslt.
    Args:
        *args:
        **kwargs:

    Returns:
        HTML

    """
    return _render_xml_as_html(XSLType.type_list, *args, **kwargs)


@register.simple_tag(name="xsl_transform_detail")
def render_xml_as_html_detail(*args, **kwargs):
    """Render an XML to HTML using the detail xslt.
    Args:
        *args:
        **kwargs:

    Returns:
        HTML

    """
    return _render_xml_as_html(XSLType.type_detail, *args, **kwargs)


def _render_xml_as_html(xslt_type, *args, **kwargs):
    """Render an XML to HTML according to an xslt type (list or detail).
    Args:
        xslt_type
        *args:
        **kwargs:

    Returns:
        HTML

    """

    xml_string = kwargs["xml_content"]
    template_id = kwargs.get("template_id", None)
    template_hash = kwargs.get("template_hash", None)
    xsl_transform_id = kwargs.get("xslt_id", None)

    try:
        try:
            if xslt_type not in (XSLType.type_list, XSLType.type_detail):
                raise Exception(
                    "XSLT Type unknown. Default xslt will be used."
                )
            if xsl_transform_id:
                xsl_transformation = xsl_transformation_api.get_by_id(
                    xsl_transform_id
                )
            elif template_id or template_hash:
                if template_id:
                    template_xsl_rendering = (
                        template_xsl_rendering_api.get_by_template_id(
                            template_id
                        )
                    )
                else:
                    template_xsl_rendering = (
                        template_xsl_rendering_api.get_by_template_hash(
                            template_hash
                        )
                    )

                if xslt_type == XSLType.type_list:
                    xsl_transformation = template_xsl_rendering.list_xslt
                else:
                    xsl_transformation = (
                        template_xsl_rendering.default_detail_xslt
                    )
            else:
                raise Exception(
                    "No template information provided. Default xslt will be used."
                )

            xslt_string = xsl_transformation.content

        except (Exception, exceptions.DoesNotExist):
            default_xslt_path = finders.find(DEFAULT_DATA_RENDERING_XSLT)
            xslt_string = read_file_content(default_xslt_path)

        return xsl_transform(xml_string, xslt_string)
    except Exception:
        return xml_string
