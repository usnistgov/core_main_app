""" Login page api
"""
from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.commons.exceptions import ApiError
from core_main_app.components.web_page import api as web_page_api

LOGIN_PAGE_NAME = "login"
LOGIN_PAGE_TYPE = WEB_PAGE_TYPES[LOGIN_PAGE_NAME]


def get():
    """Get the login page if exist

    Returns: login web page
    """
    return web_page_api.get(LOGIN_PAGE_NAME)


def upsert(login_page):
    """Post the login page

    Parameters:
        login_page (WebPage): Webpage for the login

    Returns: login web page
    """
    if login_page.type != LOGIN_PAGE_TYPE:
        raise ApiError(
            "Webpage type not coherent (expected: %s; actual %s"
            % (str(LOGIN_PAGE_TYPE), str(login_page.type))
        )

    return web_page_api.upsert(login_page)
