""" Unit tests for `AbstractProcessingModule` class from
`core_main_app.components.abstract_processing_module.models` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.components.abstract_processing_module import models
from tests.mocks import MockProcessingModule


class TestAbstractProcessingModuleGetClass(TestCase):
    """Unit tests for method `get_class`."""

    def setUp(self):
        """setUp"""
        self.mock_processing_class = "pkg1.pkg2.file.ProcessingClassName"
        self.mock_module = MockProcessingModule()
        self.mock_module.processing_class = self.mock_processing_class

    @patch.object(models, "importlib")
    def test_import_module_called(self, mock_importlib):
        """test_import_module_called"""
        self.mock_module.get_class()
        mock_importlib.import_module.assert_called_with(
            ".".join(self.mock_processing_class.split(".")[:-1])
        )

    @patch.object(models, "importlib")
    @patch.object(models, "getattr")
    def test_returns_instantiated_class(self, mock_getattr, mock_importlib):
        """test_returns_instantiated_class"""
        mock_module_pkg = MagicMock()
        mock_importlib.import_module.return_value = mock_module_pkg

        self.assertEqual(
            self.mock_module.get_class(),
            mock_getattr(
                mock_module_pkg, self.mock_processing_class.split(".")[-1]
            )(),
        )


class TestAbstractProcessingModuleStr(TestCase):
    """Unit tests for method `__str__`."""

    def test_returns_name_attribute(self):
        """test_returns_name_attribute"""
        mock_module = MockProcessingModule()
        mock_module.name = "mock_name"

        self.assertEqual(str(mock_module), mock_module.name)
