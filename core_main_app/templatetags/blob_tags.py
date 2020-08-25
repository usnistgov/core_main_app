""" Blob tags
"""
import re

from django import template

from core_main_app.utils.urls import get_blob_download_regex

register = template.Library()


@register.simple_tag(name="render_blob_links_in_span")
def render_blob_links_in_span(*args, **kwargs):
    """Find all blobs link then frame then with <span>

    Args:
        *args:
        **kwargs:

    Returns:

    """
    xml_string = kwargs["xml_string"]
    # get all blobs link
    url_blobs = re.findall(get_blob_download_regex(), xml_string)
    # we attend to frame then with a specific class selector
    blob_html_pattern = "<span class='blob-link' data-blob-url=\"{0}\">{0}</span>"
    # for all urls found, we apply the pattern
    for url in url_blobs:
        xml_string = xml_string.replace(url, blob_html_pattern.format(url))
    return xml_string
