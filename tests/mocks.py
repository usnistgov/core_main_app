""" Mock classes for use in unit tests.
"""

from unittest.mock import Mock

from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)
from core_main_app.utils.processing_module.models import (
    AbstractObjectProcessing,
)


class MockQuerySet(Mock):
    """Mock Query Set"""

    item_list = []

    def count(self):
        """Count the number of items in the queryset"""
        return len(self.item_list)

    def __getitem__(self, item):
        """Iter items"""
        return self.item_list[item]


class MockProcessingModule(AbstractProcessingModule):
    """Mock implementation of an AbstractProcessingModule Django model."""

    pass


class MockObjectProcessingModule(AbstractObjectProcessing):
    """Mock implementation of an AbstractObjectProcessing class."""

    pass
