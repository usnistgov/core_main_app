"""Results paginator util
"""
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from core_main_app.settings import RESULTS_PER_PAGE


class ResultsPaginator:
    """Results Paginator"""

    @staticmethod
    def get_results(results_list, page, results_per_page=RESULTS_PER_PAGE):
        """get_results

        Args:
            results_list:
            page:
            results_per_page:

        Returns:
        """
        # Pagination
        paginator = Paginator(results_list, results_per_page)

        try:
            results = paginator.page(int(page))
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return results
