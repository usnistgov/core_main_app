""" lxml URI resolver using requests api
"""
import logging

from core_main_app.utils.requests_utils.requests_utils import send_get_request
from xml_utils.xml_validation.resolvers.default_uri_resolver import DefaultURIResolver

logger = logging.getLogger(__name__)


class RequestsResolver(DefaultURIResolver):
    """ Requests URI Resolver for lxml
    """
    def resolve(self, url, id, context):
        """ Resolve the URI using the requests api

        Args:
            url:
            id:
            context:

        Returns:

        """
        try:
            response = send_get_request(url)
            return self.resolve_string(response.content, context)
        except Exception as e:
            # if an error occurs return None to use the next registered resolver (or lxml default resolver)
            logger.error("An error occurred with the RequestsResolver. Please make sure HTTPS is properly configured.")
            return None
