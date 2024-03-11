""" XSD Flattener Database or URL class
"""
from urllib.parse import urlparse

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.utils.urls import get_template_download_pattern
from core_main_app.utils.xsd_flattener.xsd_flattener_requests_url import (
    XSDFlattenerRequestsURL,
)
from xml_utils.xsd_flattener.xsd_flattener_url import XSDFlattenerURL


class XSDFlattenerDatabaseOrURL(XSDFlattenerRequestsURL):
    """Get the content of the dependency from the database or from the URL."""

    def __init__(self, xml_string, request, download_enabled=True):
        """Initializes the flattener

        Args:
            xml_string:
            download_enabled:
            request:
        """
        self.request = request
        XSDFlattenerURL.__init__(
            self, xml_string=xml_string, download_enabled=download_enabled
        )

    def get_dependency_content(self, uri):
        """Get the content of the dependency from the database or from the URL. Try to get the content from the
        database first and then try to download it from the provided URI.

        Args:
            uri: Content URI.

        Returns:
            Content.

        """
        # parse url
        url = urlparse(uri)
        # get pattern to match a template download url
        pattern = get_template_download_pattern()
        # match url
        match = pattern.match(url.path)
        # if match
        if match:
            try:
                # get pk from match
                object_id = match.group("pk")
                # get template object using pk
                template = template_api.get_by_id(
                    object_id, request=self.request
                )
                # get template content
                content = template.content
            except (exceptions.DoesNotExist, exceptions.ModelError, Exception):
                content = super().get_dependency_content(uri)
        else:
            content = super().get_dependency_content(uri)

        return content
