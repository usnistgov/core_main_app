"""Pagination configuration for rest_framework
"""
from rest_framework.pagination import PageNumberPagination

from core_main_app.settings import RESULTS_PER_PAGE
from core_main_app.utils.pagination.mongoengine_paginator.paginator import (
    MongoenginePaginator,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = RESULTS_PER_PAGE
    django_paginator_class = MongoenginePaginator
