""" Blob tags
"""

from django import template

from core_main_app import settings
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

    # Retrieve blob links using the default download URL
    url_blobs = get_blob_download_regex(xml_string)

    # Retrieve blob links using PID if the app is installed
    if "core_linked_records_app" in settings.INSTALLED_APPS:
        from core_linked_records_app.utils import blob as pid_blob_utils

        url_blobs += pid_blob_utils.get_blob_download_regex(xml_string)

    # Apply special template for the blob urls found
    blob_html_pattern = "<span class='blob-link' data-blob-url=\"{0}\">{0}</span>"

    for url in url_blobs:
        xml_string = xml_string.replace(url, blob_html_pattern.format(url))

    return xml_string
