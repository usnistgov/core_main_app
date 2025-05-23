""" Apps test class
"""

from unittest import TestCase
from unittest.mock import patch

from django.test import override_settings

from core_main_app.apps import _check_settings, _init_blob_modules_signals
from core_main_app.commons.exceptions import CoreError


class TestCheckSettings(TestCase):
    """TestCheckSettings"""

    @override_settings(
        CELERYBEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler"
    )
    def test_check_settings_celerybeat_scheduler_properly_set(self):
        """test_check_settings_celerybeat_scheduler_properly_set

        Returns:

        """
        _check_settings()

    @override_settings(CELERYBEAT_SCHEDULER="test")
    def test_check_settings_celerybeat_scheduler_improperly_set_raises_error(
        self,
    ):
        """test_check_settings_celerybeat_scheduler_improperly_set_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()

    @override_settings(
        ACCOUNT_ADAPTER="core_main_app.utils.allauth.cdcs_adapter.AccountAdapter",
    )
    def test_check_settings_raises_attribute_error_if_account_adapter_improperly_set(
        self,
    ):
        """test_check_settings_raises_attribute_error_if_account_adapter_improperly_set

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()

    @override_settings(
        ACCOUNT_FORMS={"signup": "WrongClass"},
    )
    def test_check_settings_raises_core_error_if_account_signup_form_class_improperly_set(
        self,
    ):
        """test_check_settings_raises_core_error_if_account_signup_form_class_improperly_set

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()

    @override_settings(
        SOCIALACCOUNT_FORMS={"signup": "WrongClass"},
    )
    def test_check_settings_raises_core_error_if_social_account_signup_form_class_improperly_set(
        self,
    ):
        """test_check_settings_raises_core_error_if_social_account_signup_form_class_improperly_set

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()

    @override_settings(
        INSTALLED_APPS=["allauth"],
    )
    def test_check_settings_allauth_without_core_website_app_raises_core_error(
        self,
    ):
        """test_check_settings_allauth_without_core_website_app_raises_core_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()


class TestInitBlobProcessingModules(TestCase):
    """TestInitBlobProcessingModules"""

    @patch(
        "core_main_app.apps.main_settings.ENABLE_BLOB_MODULES_SIGNALS", True
    )
    @patch("core_main_app.components.blob_processing_module.signals")
    def test_signals_connected_if_setting_true(
        self,
        mock_signals,
    ):
        """test_signals_connected_if_setting_true

        Returns:

        """
        _init_blob_modules_signals()

        self.assertTrue(mock_signals.connect.called)

    @patch(
        "core_main_app.apps.main_settings.ENABLE_BLOB_MODULES_SIGNALS", False
    )
    @patch("core_main_app.components.blob_processing_module.signals")
    def test_signals_not_connected_if_setting_false(self, mock_signals):
        """test_signals_not_connected_if_setting_false

        Returns:

        """
        _init_blob_modules_signals()

        self.assertFalse(mock_signals.called)
