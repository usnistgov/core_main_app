"""Pagination utils for rest_framework package
"""
from urllib.parse import urlparse

from core_main_app.commons.exceptions import PaginationError
from core_main_app.utils.pagination.rest_framework_paginator.pagination import (
    StandardResultsSetPagination,
)


def get_page_number(page):
    """Get page number from page

    Args:
        page: url, page number or None

    Returns:

    """
    if page is None:
        return None

    if isinstance(page, int):
        return page

    try:
        # parse string url
        object_url = urlparse(page)
        # get query from url
        query_url = object_url.query
        # rest framework returns base (without 'page=') url when page is 1
        if "page=" not in query_url:
            return 1

        return int(query_url.split("=")[1])
    except Exception as exception:
        return PaginationError(
            f"An error occurred when getting page number from url: {str(exception)}."
        )


def get_paginator():
    """Create a paginator

    Returns:

    """
    # return paginator
    return StandardResultsSetPagination()
