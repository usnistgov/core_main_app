"""Custom context processor
"""
from django.conf import settings


def domain_context_processor(request):
    return {
        "WEBSITE_ADMIN_COLOR": settings.WEBSITE_ADMIN_COLOR if hasattr(settings, "WEBSITE_ADMIN_COLOR") else 'black',
        "WEBSITE_SHORT_TITLE": settings.WEBSITE_SHORT_TITLE if hasattr(settings, "WEBSITE_SHORT_TITLE") else '',

        'CUSTOM_TITLE': settings.CUSTOM_TITLE if hasattr(settings, 'CUSTOM_TITLE') else '',
        'CUSTOM_ORGANIZATION': settings.CUSTOM_ORGANIZATION if hasattr(settings, 'CUSTOM_ORGANIZATION') else '',
        'CUSTOM_NAME': settings.CUSTOM_NAME if hasattr(settings, 'CUSTOM_NAME') else '',
        'CUSTOM_SUBTITLE': settings.CUSTOM_SUBTITLE if hasattr(settings, 'CUSTOM_SUBTITLE') else '',
        'CUSTOM_DATA': settings.CUSTOM_DATA if hasattr(settings, 'CUSTOM_DATA') else '',
        'CUSTOM_CURATE': settings.CUSTOM_CURATE if hasattr(settings, 'CUSTOM_CURATE') else '',
        'CUSTOM_EXPLORE': settings.CUSTOM_EXPLORE if hasattr(settings, 'CUSTOM_EXPLORE') else '',
        'CUSTOM_COMPOSE': settings.CUSTOM_COMPOSE if hasattr(settings, 'CUSTOM_COMPOSE') else '',
        'CUSTOM_URL': settings.CUSTOM_URL if hasattr(settings, 'CUSTOM_URL') else '',
        'USE_EMAIL': settings.USE_EMAIL is True if hasattr(settings, 'USE_EMAIL') else False,

        'DATA_SOURCES_EXPLORE_APPS': settings.DATA_SOURCES_EXPLORE_APPS if
        hasattr(settings, 'DATA_SOURCES_EXPLORE_APPS') else [],

        'INSTALLED_APPS': settings.INSTALLED_APPS if hasattr(settings, 'INSTALLED_APPS') else [],
    }
