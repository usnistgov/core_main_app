"""Unit tests for `core_main_app.components.data_processing_module.signals` package."""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.data.models import Data
from core_main_app.components.data_processing_module import (
    signals as data_processing_module_signals,
)


class TestConnect(TestCase):
    """Unit test for `connect` function."""

    @patch(
        "core_main_app.components.data_processing_module.signals.models_signals"
    )
    def test_connect_calls_signals_connect_functions(
        self, mock_models_signals
    ):
        """test_connect_calls_signals_connect_functions"""
        data_processing_module_signals.connect()

        self.assertTrue(mock_models_signals.post_save.connect.called)
        self.assertTrue(mock_models_signals.pre_delete.connect.called)


class TestPostSaveData(TestCase):
    """Unit test for `post_save_data` function."""

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_data_calls_process_data(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_data_calls_process_data"""
        mock_data = MagicMock()
        data_processing_module_signals.post_save_data(
            sender=Data,
            instance=mock_data,
        )

        self.assertTrue(mock_process_data_with_all_modules.apply_async.called)

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_data_created_true_calls_with_create(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_data_created_false_calls_with_create"""
        mock_data = MagicMock()
        data_processing_module_signals.post_save_data(
            sender=Data, instance=mock_data, created=True
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "CREATE",
        )

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_data_created_false_calls_with_update(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_data_created_false_calls_with_update"""
        mock_data = MagicMock()
        data_processing_module_signals.post_save_data(
            sender=Data, instance=mock_data, created=False
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "UPDATE",
        )

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_no_created_field_calls_with_update(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_no_created_field_calls_with_update"""
        mock_data = MagicMock()
        data_processing_module_signals.post_save_data(
            sender=Data, instance=mock_data, created=False
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "UPDATE",
        )

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_calls_with_instance_fields(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_calls_with_instance_fields"""
        mock_data = MagicMock(pk=1, user_id=1)
        data_processing_module_signals.post_save_data(
            sender=Data,
            instance=mock_data,
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                0
            ],
            mock_data.pk,
        )
        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                2
            ],
            mock_data.user_id,
        )

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_post_save_calls_raises_api_error_if_error_occurs(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_calls_raises_api_error_if_error_occurs"""
        mock_data = MagicMock(pk=1, user_id=1)
        mock_process_data_with_all_modules.apply_async.side_effect = ApiError(
            "error"
        )
        with self.assertRaises(ApiError):
            data_processing_module_signals.post_save_data(
                sender=Data,
                instance=mock_data,
            )


class TestPreDeleteData(TestCase):
    """Unit test for `pre_delete_data` function."""

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_pre_delete_calls_with_delete(
        self, mock_process_data_with_all_modules
    ):
        """test_pre_delete_calls_with_delete"""
        mock_data = MagicMock()
        data_processing_module_signals.pre_delete_data(
            sender=Data,
            instance=mock_data,
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "DELETE",
        )

    @patch(
        "core_main_app.components.data_processing_module.tasks.process_data_with_all_modules"
    )
    def test_pre_delete_calls_with_instance_fields(
        self, mock_process_data_with_all_modules
    ):
        """test_post_save_calls_with_instance_fields"""
        mock_data = MagicMock(pk=1, user_id=1)
        data_processing_module_signals.pre_delete_data(
            sender=Data,
            instance=mock_data,
        )

        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                0
            ],
            mock_data.pk,
        )
        self.assertEqual(
            mock_process_data_with_all_modules.apply_async.call_args.args[0][
                2
            ],
            mock_data.user_id,
        )
