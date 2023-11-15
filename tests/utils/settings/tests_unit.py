""" Unit tests for `core_main_app.utils.settings` package."""
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from core_main_app.utils import settings as settings_utils


class TestGetAttrFromDeprecatedVar(TestCase):
    """Unit tests for `getattr_from_deprecated_var` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "input_settings": MagicMock(),
            "deprecated_var_name": MagicMock(),
            "supported_var_name": MagicMock(),
            "default_value": MagicMock(),
        }

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_getattr_called(
        self,
        mock_getattr,
        mock_logger,  # noqa, pylint: disable=unused-argument
    ):
        """test_getattr_called"""
        settings_utils.getattr_from_deprecated_var(**self.mock_kwargs)

        mock_getattr.assert_has_calls(
            [
                call(
                    self.mock_kwargs["input_settings"],
                    self.mock_kwargs["deprecated_var_name"],
                ),
                call(
                    self.mock_kwargs["input_settings"],
                    self.mock_kwargs["supported_var_name"],
                ),
            ]
        )

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_deprecated_var_value_set_triggers_warning(
        self, mock_getattr, mock_logger
    ):
        """test_deprecated_var_value_set_triggers_warning"""
        mock_deprecated_setting_val = "mock_settings_old_value"
        mock_getattr.side_effect = [
            mock_deprecated_setting_val,
            AttributeError("mock_attribute_error"),
        ]
        settings_utils.getattr_from_deprecated_var(**self.mock_kwargs)

        self.assertEqual(mock_logger.warning.call_count, 1)

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_deprecated_and_supported_var_value_set_triggers_warning(
        self, mock_getattr, mock_logger
    ):
        """test_deprecated_and_supported_var_value_set_triggers_warning"""
        mock_setting_val = "mock_settings_value"
        mock_getattr.side_effect = [mock_setting_val, mock_setting_val]
        settings_utils.getattr_from_deprecated_var(**self.mock_kwargs)

        self.assertEqual(mock_logger.warning.call_count, 2)

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_supported_var_value_not_set_returns_deprecated_var_value(
        self,
        mock_getattr,
        mock_logger,  # noqa, pylint: disable=unused-argument
    ):
        """test_supported_var_value_not_set_returns_deprecated_var_value"""
        mock_deprecated_setting_val = "mock_settings_old_value"
        mock_getattr.side_effect = [
            mock_deprecated_setting_val,
            AttributeError("mock_attribute_error"),
        ]

        self.assertEqual(
            settings_utils.getattr_from_deprecated_var(**self.mock_kwargs),
            mock_deprecated_setting_val,
        )

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_supported_and_deprecated_var_value_not_set_returns_default_value(
        self,
        mock_getattr,
        mock_logger,  # noqa, pylint: disable=unused-argument
    ):
        """test_supported_and_deprecated_var_value_not_set_returns_default_value"""
        mock_getattr.side_effect = [
            AttributeError("mock_attribute_error"),
            AttributeError("mock_attribute_error"),
        ]

        self.assertEqual(
            settings_utils.getattr_from_deprecated_var(**self.mock_kwargs),
            self.mock_kwargs["default_value"],
        )

    @patch.object(settings_utils, "logger")
    @patch.object(settings_utils, "getattr")
    def test_supported_var_value_set_returns_supported_var_value(
        self,
        mock_getattr,
        mock_logger,  # noqa, pylint: disable=unused-argument
    ):
        """test_supported_var_value_set_returns_supported_var_value"""
        mock_new_setting_val = "mock_settings_new_value"
        mock_getattr.side_effect = [
            "mock_settings_old_value",
            mock_new_setting_val,
        ]

        self.assertEqual(
            settings_utils.getattr_from_deprecated_var(**self.mock_kwargs),
            mock_new_setting_val,
        )
