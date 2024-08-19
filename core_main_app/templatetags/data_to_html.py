""" Convert data to HTML
"""

import json
import logging

from django import template as django_template

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)
from core_main_app.utils import xml as main_xml_utils

register = django_template.Library()

logger = logging.getLogger(__name__)


def _render_data_html(html_rendering, dict_content):
    """Render data's dict content with html template

    Args:
        html_rendering:
        dict_content:

    Returns:

    """
    # load html with django template
    django_template_obj = django_template.Template(html_rendering)
    # render template
    return django_template_obj.render(
        context=django_template.Context({"dict_content": dict_content})
    )


def _get_template_html_rendering(
    template_id=None, template_hash=None, rendering_type="detail"
):
    """Get a template HTML rendering from id or hash

    Args:
        template_id:
        template_hash:
        rendering_type: detail or list

    Returns:

    """
    # if template id is set, get rendering by template id
    if template_id:
        template_html_rendering = (
            template_html_rendering_api.get_by_template_id(template_id)
        )
    # if template hash is set, get rendering by template hash
    elif template_hash:
        template_html_rendering = (
            template_html_rendering_api.get_by_template_hash(template_hash)
        )
    # if no template information, return None
    else:
        return None
    # return detail or list rendering set
    if rendering_type == "detail":
        return template_html_rendering.detail_rendering
    elif rendering_type == "list":
        return template_html_rendering.list_rendering
    else:
        return None


def _data_content_to_dict(data_content, template_format):
    """Get dict content from data content

    Args:
        data_content:
        template_format:

    Returns:

    """
    # if data is JSON
    if template_format == Template.JSON:
        # convert JSON string to dict
        return json.loads(data_content)
    # if the data is XML
    elif template_format == Template.XSD:
        # convert XML string to dict
        return main_xml_utils.raw_xml_to_dict(data_content)
    # if unknown data format, raise an exception
    else:
        raise NotImplementedError("Unsupported format.")


@register.simple_tag(name="data_detail_html")
def data_detail_html(data):
    """Transform data to html

    Args:
        data:

    Returns: html rendering or None

    """
    template_hash = None
    template_format = None

    # if data is a Data object
    if isinstance(data, Data):
        # get template from data
        template_id = data.template
        # get dict_content from data
        data_content = data.get_dict_content()
    # if data is dict
    elif isinstance(data, dict):
        # get template id from data["template"]["id"]
        template_id = data["template"].get("id", None)
        # if template id was not provided
        if not template_id:
            # get template hash from data["template"]["hash"]
            template_hash = data["template"].get("hash", None)
        # get template format from data["template"]["format"]
        template_format = data["template"].get("format", None)
        # get data content
        data_content = data["content"]
    # if other type, return None
    else:
        return None
    try:
        # get detail html rendering for this template
        template_html_rendering = _get_template_html_rendering(
            template_id=template_id,
            template_hash=template_hash,
            rendering_type="detail",
        )
        # if template html rendering not set, return None
        if not template_html_rendering:
            return None
        # if the data content is not a dict (template context expects a dict)
        if not isinstance(data_content, dict):
            data_content = _data_content_to_dict(data_content, template_format)
        # render the data with the HTML template
        return _render_data_html(template_html_rendering, data_content)
    except DoesNotExist:
        # no template html rendering found
        return None
    except Exception as e:
        logger.error(
            "An error occurred while rendering data to html: " + str(e)
        )
        return None
