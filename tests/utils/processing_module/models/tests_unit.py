""" Unit tests for `AbstractObjectProcessing` class from `core_main_app.blob_modules`
package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.abstract_processing_module.models import (
    AbstractProcessingModule,
)
from tests.mocks import MockObjectProcessingModule


class TestAbstractObjectProcessingProcess(TestCase):
    """Unit tests for `AbstractObjectProcessing.process` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    @patch("tests.mocks.MockObjectProcessingModule._process_on_demand")
    def test_process_on_demand_called_for_proper_strategy(
        self, mock_process_on_demand
    ):
        """test_process_on_demand_called_for_proper_strategy"""
        self.object_processing_module.process(
            **{
                "strategy": AbstractProcessingModule.RUN_ON_DEMAND,
                **self.mock_kwargs,
            }
        )

        mock_process_on_demand.assert_called_with(
            self.mock_kwargs["db_object"], self.mock_kwargs["module_params"]
        )

    @patch("tests.mocks.MockObjectProcessingModule._process_on_create")
    def test_process_on_create_called_for_proper_strategy(
        self, mock_process_on_create
    ):
        """test_process_on_create_called_for_proper_strategy"""
        self.object_processing_module.process(
            **{
                "strategy": AbstractProcessingModule.RUN_ON_CREATE,
                **self.mock_kwargs,
            }
        )

        mock_process_on_create.assert_called_with(
            self.mock_kwargs["db_object"], self.mock_kwargs["module_params"]
        )

    @patch("tests.mocks.MockObjectProcessingModule._process_on_read")
    def test_process_on_read_called_for_proper_strategy(
        self, mock_process_on_read
    ):
        """test_process_on_read_called_for_proper_strategy"""
        self.object_processing_module.process(
            **{
                "strategy": AbstractProcessingModule.RUN_ON_READ,
                **self.mock_kwargs,
            }
        )

        mock_process_on_read.assert_called_with(
            self.mock_kwargs["db_object"], self.mock_kwargs["module_params"]
        )

    @patch("tests.mocks.MockObjectProcessingModule._process_on_update")
    def test_process_on_update_called_for_proper_strategy(
        self, mock_process_on_update
    ):
        """test_process_on_update_called_for_proper_strategy"""
        self.object_processing_module.process(
            **{
                "strategy": AbstractProcessingModule.RUN_ON_UPDATE,
                **self.mock_kwargs,
            }
        )

        mock_process_on_update.assert_called_with(
            self.mock_kwargs["db_object"], self.mock_kwargs["module_params"]
        )

    @patch("tests.mocks.MockObjectProcessingModule._process_on_delete")
    def test_process_on_delete_called_for_proper_strategy(
        self, mock_process_on_delete
    ):
        """test_process_on_delete_called_for_proper_strategy"""
        self.object_processing_module.process(
            **{
                "strategy": AbstractProcessingModule.RUN_ON_DELETE,
                **self.mock_kwargs,
            }
        )

        mock_process_on_delete.assert_called_with(
            self.mock_kwargs["db_object"], self.mock_kwargs["module_params"]
        )

    def test_unknown_strategy_raises_processing_module_exception(self):
        """test_unknown_strategy_raises_processing_module_exception"""
        with self.assertRaises(CoreError):
            self.object_processing_module.process(
                **{
                    "strategy": "mock_unknown_strategy",
                    **self.mock_kwargs,
                }
            )


class TestAbstractObjectProcessingProcessOnDemand(TestCase):
    """Unit tests for `AbstractObjectProcessing._process_on_demand` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    def test_process_on_demand_raise_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.object_processing_module._process_on_demand(
                **self.mock_kwargs
            )


class TestAbstractObjectProcessingProcessOnCreate(TestCase):
    """Unit tests for `AbstractObjectProcessing._process_on_create` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    def test_process_on_create_raise_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.object_processing_module._process_on_create(
                **self.mock_kwargs
            )


class TestAbstractObjectProcessingProcessOnRead(TestCase):
    """Unit tests for `AbstractObjectProcessing._process_on_read` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    def test_process_on_read_raise_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.object_processing_module._process_on_read(**self.mock_kwargs)


class TestAbstractObjectProcessingProcessOnUpdate(TestCase):
    """Unit tests for `AbstractObjectProcessing._process_on_update` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    def test_process_on_update_raise_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.object_processing_module._process_on_update(
                **self.mock_kwargs
            )


class TestAbstractObjectProcessingProcessOnDelete(TestCase):
    """Unit tests for `AbstractObjectProcessing._process_on_delete` method"""

    def setUp(self):
        """setUp"""
        self.object_processing_module = MockObjectProcessingModule()

        self.mock_kwargs = {
            "db_object": MagicMock(),
            "module_params": MagicMock(),
        }

    def test_process_on_delete_raise_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.object_processing_module._process_on_delete(
                **self.mock_kwargs
            )
