"""XSL Transformation tag
"""
from django import template
from os.path import join

from django.contrib.staticfiles import finders
from core_main_app.utils.xml import xsl_transform

register = template.Library()


@register.filter(name='xsl_transform')
def render_xml_as_html(xml_string, template_id=None):
    try:
        if template_id is not None:
            # TODO: find custom XSLT attached to template and use it for transformation
            return xml_string
        else:
            default_xslt_path = finders.find(join('core_main_app', 'common', 'xsl', 'xml2html.xsl'))
            xslt_string = _read_file_content(default_xslt_path)
            return xsl_transform(xml_string, xslt_string)
    except:
        return xml_string


def _read_file_content(file_path):
    """Reads the content of a file

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content
