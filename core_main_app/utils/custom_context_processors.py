"""Custom context processor
"""
from django.conf import settings


def domain_context_processor(request):
    """domain_context_processor

    Args:
        request:

    Returns
    """

    return {
        "WEBSITE_ADMIN_COLOR": settings.WEBSITE_ADMIN_COLOR
        if hasattr(settings, "WEBSITE_ADMIN_COLOR")
        else "black",
        "WEBSITE_SHORT_TITLE": settings.WEBSITE_SHORT_TITLE
        if hasattr(settings, "WEBSITE_SHORT_TITLE")
        else "",
        "CUSTOM_TITLE": settings.CUSTOM_TITLE
        if hasattr(settings, "CUSTOM_TITLE")
        else "",
        "CUSTOM_ORGANIZATION": settings.CUSTOM_ORGANIZATION
        if hasattr(settings, "CUSTOM_ORGANIZATION")
        else "",
        "CUSTOM_NAME": settings.CUSTOM_NAME,
        "CUSTOM_SUBTITLE": settings.CUSTOM_SUBTITLE
        if hasattr(settings, "CUSTOM_SUBTITLE")
        else "",
        "CUSTOM_DATA": settings.CUSTOM_DATA if hasattr(settings, "CUSTOM_DATA") else "",
        "CUSTOM_URL": settings.CUSTOM_URL if hasattr(settings, "CUSTOM_URL") else "",
        "DATA_SOURCES_EXPLORE_APPS": settings.DATA_SOURCES_EXPLORE_APPS
        if hasattr(settings, "DATA_SOURCES_EXPLORE_APPS")
        else [],
        "INSTALLED_APPS": settings.INSTALLED_APPS
        if hasattr(settings, "INSTALLED_APPS")
        else [],
        "DISPLAY_NIST_HEADERS": settings.DISPLAY_NIST_HEADERS
        if hasattr(settings, "DISPLAY_NIST_HEADERS")
        else False,
    }
