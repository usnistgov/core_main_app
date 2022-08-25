""" lxml URI resolver using requests api
"""
import logging

from xml_utils.xml_validation.resolvers.default_uri_resolver import DefaultURIResolver
from core_main_app.utils.requests_utils.requests_utils import send_get_request

logger = logging.getLogger(__name__)


class RequestsResolver(DefaultURIResolver):
    """Requests URI Resolver for lxml"""

    session_id = None

    def __init__(self, session_id=None):
        super().__init__()
        self.session_id = session_id

    def resolve(self, url, id, context):
        """Resolve the URI using the requests api

        Args:
            url:
            id:
            context:

        Returns:

        """
        try:
            response = send_get_request(url, cookies={"sessionid": self.session_id})
            return self.resolve_string(response.content, context)
        except Exception:
            # if an error occurs return None to use the next registered resolver (or lxml default resolver)
            logger.error(
                "An error occurred with the RequestsResolver. Please make sure HTTPS is properly configured."
            )
            return None
