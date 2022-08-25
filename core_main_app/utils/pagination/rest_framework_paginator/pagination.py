"""Pagination configuration for rest_framework
"""
from rest_framework.pagination import PageNumberPagination

from core_main_app.settings import RESULTS_PER_PAGE, MONGODB_INDEXING
from core_main_app.utils.pagination.mongoengine_paginator.paginator import (
    MongoenginePaginator,
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard Results Set Pagination"""

    page_size = RESULTS_PER_PAGE
    if MONGODB_INDEXING:
        django_paginator_class = MongoenginePaginator
