"""Pagination utils for rest_framework package
"""
from urlparse import urlparse
from core_explore_common_app.commons.exceptions import PaginationError
from core_main_app.utils.pagination.rest_framework_paginator.pagination import StandardResultsSetPagination


def get_page_number(url):
    """Get page number from url

    Args:
        url:

    Returns:

    """

    if url is None:
        return None

    try:
        # parse string url
        object_url = urlparse(url)
        # get query from url
        query_url = object_url.query
        # rest framework returns base (without 'page=') url when page is 1
        if "page=" not in query_url:
            return 1
        else:
            return query_url.split('=')[1]
    except Exception, e:
        return PaginationError("An error occurred when getting page number from url: {}.".format(e.message))


def get_paginator():
    """Create a paginator

    Returns:

    """
    # return paginator
    return StandardResultsSetPagination()
