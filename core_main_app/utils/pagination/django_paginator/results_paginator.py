"""Results paginator util
"""
from django.core.paginator import PageNotAnInteger, EmptyPage

from core_main_app.settings import RESULTS_PER_PAGE
from core_main_app.utils.pagination.mongoengine_paginator.paginator import (
    MongoenginePaginator,
)


class ResultsPaginator(object):
    @staticmethod
    def get_results(results_list, page, results_per_page=RESULTS_PER_PAGE):
        # Pagination
        paginator = MongoenginePaginator(results_list, results_per_page)

        try:
            results = paginator.page(int(page))
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return results
