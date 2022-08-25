""" XSD Flattener Requests URL Class
"""
from xml_utils.xsd_flattener.xsd_flattener_url import XSDFlattenerURL
from core_main_app.utils.requests_utils.requests_utils import send_get_request


class XSDFlattenerRequestsURL(XSDFlattenerURL):
    """Get the content of the dependency from the database or from the URL."""

    def __init__(self, xml_string, download_enabled=True):
        """Initializes the flattener

        Args:
            xml_string:
            download_enabled:
        """
        XSDFlattenerURL.__init__(
            self, xml_string=xml_string, download_enabled=download_enabled
        )

    def get_dependency_content(self, uri):
        """Get the content of the dependency from the URL using request util for HTTPS compliance

        Args:
            uri: Content URI

        Returns:
            Content

        """
        if self.download_enabled:
            dependency_file = send_get_request(uri)
            return dependency_file.content
        return ""
