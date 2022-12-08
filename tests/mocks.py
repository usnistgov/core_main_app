""" Mock classes for use in unit tests.
"""
from unittest.mock import Mock


class MockQuerySet(Mock):
    """Mock Query Set"""

    item_list = []

    def count(self):
        """Count the number of items in the queryset"""
        return len(self.item_list)

    def __getitem__(self, item):
        """Iter items"""
        return self.item_list[item]
