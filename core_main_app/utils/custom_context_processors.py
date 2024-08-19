""" Custom context processor to generate global variables to be used in templates.
"""

from django.conf import settings
from django.template import RequestContext

from core_main_app.commons.constants import AVAILABLE_BOOTSTRAP_VERSIONS


def domain_context_processor(
    request: RequestContext,  # noqa, pylint: disable=unused-argument
):
    """Returns the additional variables to be sent with the context

    Args:
        request (RequestContext): The request to be processed by the template.

    Returns:
        dict: Additional variables to be injected into the context.
    """

    return {
        "WEBSITE_ADMIN_COLOR": getattr(
            settings, "WEBSITE_ADMIN_COLOR", "black"
        ),
        "WEBSITE_SHORT_TITLE": getattr(settings, "WEBSITE_SHORT_TITLE", ""),
        "CUSTOM_TITLE": getattr(settings, "CUSTOM_TITLE", ""),
        "CUSTOM_ORGANIZATION": getattr(settings, "CUSTOM_ORGANIZATION", ""),
        "CUSTOM_NAME": getattr(settings, "CUSTOM_NAME"),
        "CUSTOM_SUBTITLE": getattr(settings, "CUSTOM_SUBTITLE", ""),
        "CUSTOM_DATA": getattr(settings, "CUSTOM_DATA", ""),
        "CUSTOM_URL": getattr(settings, "CUSTOM_URL", ""),
        "DATA_SOURCES_EXPLORE_APPS": getattr(
            settings, "DATA_SOURCES_EXPLORE_APPS", []
        ),
        "INSTALLED_APPS": getattr(settings, "INSTALLED_APPS"),
        "DISPLAY_NIST_HEADERS": getattr(
            settings, "DISPLAY_NIST_HEADERS", False
        ),
        "LOGIN_URL": getattr(settings, "LOGIN_URL", ""),
        "BOOTSTRAP_VERSION": (
            settings.BOOTSTRAP_VERSION
            if hasattr(settings, "BOOTSTRAP_VERSION")
            and settings.BOOTSTRAP_VERSION in AVAILABLE_BOOTSTRAP_VERSIONS
            else "4.6.2"
        ),
        "PROJECT_VERSION": getattr(settings, "PROJECT_VERSION", "0.0.0"),
    }
