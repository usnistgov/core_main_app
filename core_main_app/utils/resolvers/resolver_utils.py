""" LXML URI Resolver utils
"""
from logging import getLogger

from core_main_app.commons.exceptions import CoreError
from core_main_app.settings import XSD_URI_RESOLVER
from core_main_app.utils.resolvers.xsd_uri_resolvers import XSD_URI_RESOLVERS

logger = getLogger(__name__)


def lmxl_uri_resolver(*args, **kwargs):
    """Return lxml uri resolver according to the settings


    Returns:

    """
    uri_resolver = None
    try:
        request = kwargs.pop("request")
        session_id = request.session.session_key
    except Exception:
        logger.info("No request or session id is None")
        session_id = None

    if XSD_URI_RESOLVER:
        # Check that the setting is an accepted value
        if XSD_URI_RESOLVER not in XSD_URI_RESOLVERS:
            raise CoreError(
                "Error: XSD_URI_RESOLVER setting has an incorrect value."
            )
        # Return the correct resolver depending on the setting

        uri_resolver = XSD_URI_RESOLVERS[XSD_URI_RESOLVER](
            session_id=session_id
        )

    return uri_resolver
