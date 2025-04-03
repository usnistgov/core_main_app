""" Unit tests for `core_main_app.components.blob_processing_module.signals` package.
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_main_app.commons.exceptions import ApiError
from core_main_app.components.blob.models import Blob
from core_main_app.components.blob_processing_module import (
    signals as blob_processing_module_signals,
)


class TestConnect(TestCase):
    """Unit test for `connect` function."""

    @patch(
        "core_main_app.components.blob_processing_module.signals.models_signals"
    )
    def test_connect_calls_signals_connect_functions(
        self, mock_models_signals
    ):
        """test_connect_calls_signals_connect_functions"""
        blob_processing_module_signals.connect()

        self.assertTrue(mock_models_signals.post_save.connect.called)
        self.assertTrue(mock_models_signals.pre_delete.connect.called)


class TestPostSaveBlob(TestCase):
    """Unit test for `post_save_blob` function."""

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_blob_calls_process_blob(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_blob_calls_process_blob"""
        mock_blob = MagicMock()
        blob_processing_module_signals.post_save_blob(
            sender=Blob,
            instance=mock_blob,
        )

        self.assertTrue(mock_process_blob_with_all_modules.apply_async.called)

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_blob_created_true_calls_with_create(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_blob_created_false_calls_with_create"""
        mock_blob = MagicMock()
        blob_processing_module_signals.post_save_blob(
            sender=Blob, instance=mock_blob, created=True
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "CREATE",
        )

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_blob_created_false_calls_with_update(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_blob_created_false_calls_with_update"""
        mock_blob = MagicMock()
        blob_processing_module_signals.post_save_blob(
            sender=Blob, instance=mock_blob, created=False
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "UPDATE",
        )

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_no_created_field_calls_with_update(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_no_created_field_calls_with_update"""
        mock_blob = MagicMock()
        blob_processing_module_signals.post_save_blob(
            sender=Blob, instance=mock_blob, created=False
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "UPDATE",
        )

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_calls_with_instance_fields(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_calls_with_instance_fields"""
        mock_blob = MagicMock(pk=1, user_id=1)
        blob_processing_module_signals.post_save_blob(
            sender=Blob,
            instance=mock_blob,
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                0
            ],
            mock_blob.pk,
        )
        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                2
            ],
            mock_blob.user_id,
        )

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_post_save_calls_raises_api_error_if_error_occurs(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_calls_raises_api_error_if_error_occurs"""
        mock_blob = MagicMock(pk=1, user_id=1)
        mock_process_blob_with_all_modules.apply_async.side_effect = ApiError(
            "error"
        )
        with self.assertRaises(ApiError):
            blob_processing_module_signals.post_save_blob(
                sender=Blob,
                instance=mock_blob,
            )


class TestPreDeleteBlob(TestCase):
    """Unit test for `pre_delete_blob` function."""

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_pre_delete_calls_with_delete(
        self, mock_process_blob_with_all_modules
    ):
        """test_pre_delete_calls_with_delete"""
        mock_blob = MagicMock()
        blob_processing_module_signals.pre_delete_blob(
            sender=Blob,
            instance=mock_blob,
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                1
            ],
            "DELETE",
        )

    @patch(
        "core_main_app.components.blob_processing_module.tasks.process_blob_with_all_modules"
    )
    def test_pre_delete_calls_with_instance_fields(
        self, mock_process_blob_with_all_modules
    ):
        """test_post_save_calls_with_instance_fields"""
        mock_blob = MagicMock(pk=1, user_id=1)
        blob_processing_module_signals.pre_delete_blob(
            sender=Blob,
            instance=mock_blob,
        )

        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                0
            ],
            mock_blob.pk,
        )
        self.assertEqual(
            mock_process_blob_with_all_modules.apply_async.call_args.args[0][
                2
            ],
            mock_blob.user_id,
        )
