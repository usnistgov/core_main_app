""" Apps test class
"""
from unittest import TestCase

from django.test import override_settings

from core_main_app.apps import _check_settings
from core_main_app.commons.exceptions import CoreError


class TestCheckSettings(TestCase):
    """TestCheckSettings"""

    @override_settings(
        CELERYBEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler"
    )
    def test_check_settings_CELERYBEAT_SCHEDULER_properly_set(self):
        """test_check_settings_CELERYBEAT_SCHEDULER_properly_set

        Returns:

        """
        _check_settings()

    @override_settings(CELERYBEAT_SCHEDULER="test")
    def test_check_settings_CELERYBEAT_SCHEDULER_improperly_set_raises_error(
        self,
    ):
        """test_check_settings_CELERYBEAT_SCHEDULER_improperly_set_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()

    @override_settings(ENABLE_SAML2_SSO_AUTH=True, ENABLE_2FA=False)
    def test_check_settings_ENABLE_SAML2_SSO_AUTH_properly_set(self):
        """test_check_settings_CELERYBEAT_SCHEDULER_properly_set

        Returns:

        """
        _check_settings()

    @override_settings(ENABLE_SAML2_SSO_AUTH=False, ENABLE_2FA=True)
    def test_check_settings_ENABLE_2FA_properly_set(self):
        """test_check_settings_ENABLE_2FA_properly_set

        Returns:

        """
        _check_settings()

    @override_settings(ENABLE_SAML2_SSO_AUTH=True, ENABLE_2FA=True)
    def test_check_settings_ENABLE_SAML2_SSO_AUTH_and_ENABLE_2FA_set_raises_error(
        self,
    ):
        """test_check_settings_ENABLE_SAML2_SSO_AUTH_and_ENABLE_2FA_set_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings()
