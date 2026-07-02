"""Unit tests for `DataProcessingModule` from the
`core_main_app.components.data_processing_module.models` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_main_app.components.data_processing_module import (
    models as data_processing_module_models,
)


class TestGetById(TestCase):
    """Unit tests for `DataProcessingModule.get_by_id` method."""

    def setUp(self):
        """setUp"""
        self.data_processing_module = (
            data_processing_module_models.DataProcessingModule()
        )
        self.mock_kwargs = {"data_module_id": MagicMock()}

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_objects_get_called(self, mock_data_processing_module_objects):
        """test_objects_get_called"""
        self.data_processing_module.get_by_id(**self.mock_kwargs)

        mock_data_processing_module_objects.get.assert_called_with(
            pk=self.mock_kwargs["data_module_id"]
        )

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_object_does_not_exist_raises_does_not_exist_exception(
        self, mock_data_processing_module_objects
    ):
        """test_object_does_not_exist_raises_does_not_exist_exception"""
        mock_data_processing_module_objects.get.side_effect = (
            ObjectDoesNotExist("mock_dne_exception")
        )

        with self.assertRaises(DoesNotExist):
            self.data_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_exception_raises_model_error(
        self, mock_data_processing_module_objects
    ):
        """test_exception_raises_model_error"""
        mock_data_processing_module_objects.get.side_effect = Exception(
            "mock_objects_get_exception"
        )

        with self.assertRaises(ModelError):
            self.data_processing_module.get_by_id(**self.mock_kwargs)

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_returns_objects_get(self, mock_data_processing_module_objects):
        """test_returns_objects_get"""
        mock_module_instance = MagicMock()
        mock_data_processing_module_objects.get.return_value = (
            mock_module_instance
        )

        self.assertEqual(
            self.data_processing_module.get_by_id(**self.mock_kwargs),
            mock_module_instance,
        )


class TestGetAll(TestCase):
    """Unit tests for `DataProcessingModule.get_all` method."""

    def setUp(self):
        """setUp"""
        self.data_processing_module = (
            data_processing_module_models.DataProcessingModule()
        )

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_objects_all_called(self, mock_data_processing_module_objects):
        """test_objects_all_called"""
        self.data_processing_module.get_all()

        mock_data_processing_module_objects.all.assert_called_with()

    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.objects"
    )
    def test_returns_objects_all(self, mock_data_processing_module_objects):
        """test_returns_objects_all"""
        mock_module_list = MagicMock()
        mock_data_processing_module_objects.all.return_value = mock_module_list

        self.assertEqual(
            self.data_processing_module.get_all(), mock_module_list
        )


class TestExecuteProcess(TestCase):
    """Unit tests for `DataProcessingModule.execute_process` method."""

    def setUp(self):
        """setUp"""
        self.data_processing_module = (
            data_processing_module_models.DataProcessingModule()
        )

    @patch(
        "core_main_app.components.data_processing_module.models._suppress_processing_signals"
    )
    def test_guarded_save_sets_and_resets_signal(self, mock_suppress):
        """test_guarded_save_sets_and_resets_signal"""
        # Arrange
        mock_token = "mock_token"
        mock_suppress.set.return_value = mock_token
        mock_data = MagicMock()

        # Act
        self.data_processing_module._guarded_save(mock_data)

        # Assert
        mock_suppress.set.assert_called_once_with(True)
        mock_data.convert_and_save.assert_called_once()
        mock_suppress.reset.assert_called_once_with(mock_token)

    @patch(
        "core_main_app.components.data_processing_module.models.transaction.on_commit"
    )
    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.get_class"
    )
    def test_execute_process_saves_when_content_changes(
        self, mock_get_class, mock_on_commit
    ):
        """test_execute_process_saves_when_content_changes"""
        # Arrange
        mock_processor = MagicMock()
        mock_get_class.return_value = mock_processor
        mock_data = MagicMock()
        mock_data.content = "content"
        mock_processor.process.side_effect = (
            lambda data, *args, **kwargs: setattr(
                data, "content", "changed_content"
            )
        )

        # Act
        self.data_processing_module.execute_process(
            mock_data, strategy="CREATE"
        )

        # Assert
        mock_processor.process.assert_called_once_with(
            mock_data, strategy="CREATE"
        )
        mock_on_commit.assert_called_once()

    @patch(
        "core_main_app.components.data_processing_module.models.transaction.on_commit"
    )
    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.get_class"
    )
    def test_execute_process_does_not_save_when_content_changes_but_delete_strategy(
        self, mock_get_class, mock_on_commit
    ):
        """test_execute_process_does_not_save_when_content_changes_but_delete_strategy"""
        # Arrange
        mock_processor = MagicMock()
        mock_get_class.return_value = mock_processor
        mock_data = MagicMock()
        mock_data.content = "content"
        mock_processor.process.side_effect = (
            lambda data, *args, **kwargs: setattr(
                data, "content", "changed_content"
            )
        )

        # Act
        self.data_processing_module.execute_process(
            mock_data, strategy="DELETE"
        )

        # Assert
        mock_processor.process.assert_called_once_with(
            mock_data, strategy="DELETE"
        )
        mock_on_commit.assert_not_called()

    @patch(
        "core_main_app.components.data_processing_module.models.transaction.on_commit"
    )
    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.get_class"
    )
    def test_execute_process_does_not_save_when_content_is_same(
        self, mock_get_class, mock_on_commit
    ):
        """test_execute_process_does_not_save_when_content_is_same"""
        # Arrange
        mock_processor = MagicMock()
        mock_get_class.return_value = mock_processor
        mock_processor.process.return_value = None
        mock_data = MagicMock()

        # Act
        self.data_processing_module.execute_process(
            mock_data, strategy="CREATE"
        )

        # Assert
        mock_processor.process.assert_called_once()
        mock_on_commit.assert_not_called()

    @patch(
        "core_main_app.components.data_processing_module.models.transaction.on_commit"
    )
    @patch(
        "core_main_app.components.data_processing_module.models.DataProcessingModule.get_class"
    )
    def test_execute_process_passes_args_kwargs(
        self, mock_get_class, mock_on_commit
    ):
        """test_execute_process_passes_args_kwargs"""
        # Arrange
        mock_processor = MagicMock()
        mock_get_class.return_value = mock_processor
        mock_data = MagicMock()

        # Act
        self.data_processing_module.execute_process(
            mock_data, "extra_arg", key="value", strategy="CREATE"
        )

        # Assert
        mock_processor.process.assert_called_once_with(
            mock_data, "extra_arg", key="value", strategy="CREATE"
        )
