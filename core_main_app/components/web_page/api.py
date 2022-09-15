"""Web page API
"""
from core_main_app.commons import exceptions
from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.components.web_page.models import WebPage


def get(page_type):
    """Get the web page of a given type

    Args:
        page_type: type of the web page

    Returns: web page corresponding to the given id
    """
    if page_type not in list(WEB_PAGE_TYPES.keys()):
        return None
    try:
        return WebPage.get_by_type(page_type)
    except exceptions.DoesNotExist:
        return None


def delete_by_type(page_type):
    """Delete the web pages with the given type

    Args:
        page_type (int): page type

    Returns: Web page

    """
    return WebPage.delete_by_type(page_type)


def upsert(web_page):
    """Upsert the page content

    Args:
        web_page (obj): web page object

    Returns: content of the web page
    """
    if web_page.type not in list(WEB_PAGE_TYPES.values()):
        raise exceptions.ApiError("Web page type does not exist")

    # strip in case of whitespaces only
    if web_page.content.strip():
        # we save the object only if the content is not empty
        return web_page.save()
    else:
        # otherwise it means deletion
        return delete_by_type(web_page.type)
