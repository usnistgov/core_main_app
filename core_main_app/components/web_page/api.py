"""Web page API
"""
import core_main_app.commons.exceptions as exceptions
from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.components.web_page.models import WebPage


def get(page_type):
    """Get the web page of a given type

        Parameters:
            page_type: type of the web page

        Returns: web page corresponding to the given id
    """
    if page_type not in WEB_PAGE_TYPES.keys():
        return None
    try:
        return WebPage.get_by_type(page_type)
    except exceptions.DoesNotExist:
        return None


def upsert(web_page):
    """Post the page content

        Parameters:
            web_page (obj): web page object

        Returns: content of the web page
    """
    if web_page.type not in WEB_PAGE_TYPES.values():
        raise exceptions.ApiError("Web page type does not exist")

    return web_page.save()
