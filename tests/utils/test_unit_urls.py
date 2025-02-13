""" Urls test class
"""

from unittest import TestCase
from unittest.mock import patch

from django.test import override_settings

from core_main_app.utils.urls import get_auth_urls


class TestUrls(TestCase):
    """TestUrls"""

    @patch("core_main_app.utils.urls.main_settings")
    def test_urls_with_enable_saml2_sso_auth(self, mock_main_settings):
        """test_urls_with_enable_saml2_sso_auth

        Returns:

        """
        mock_main_settings.ENABLE_ALLAUTH = False
        mock_main_settings.ENABLE_SAML2_SSO_AUTH = True
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))
        self.assertTrue("saml2" in str(urlpatterns))

    @patch("core_main_app.utils.urls.main_settings")
    def test_urls_without_enable_saml2_sso_auth(self, mock_main_settings):
        """test_urls_without_enable_saml2_sso_auth

        Returns:

        """
        mock_main_settings.ENABLE_ALLAUTH = False
        mock_main_settings.ENABLE_SAML2_SSO_AUTH = False
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))

    @patch("core_main_app.utils.urls.main_settings")
    def test_urls_with_enable_allauth(self, mock_main_settings):
        """test_urls_with_enable_allauth

        Returns:

        """
        mock_main_settings.ENABLE_ALLAUTH = True
        mock_main_settings.ENABLE_SAML2_SSO_AUTH = False
        urlpatterns = get_auth_urls()
        self.assertTrue("accounts" in str(urlpatterns))

    @override_settings(
        INSTALLED_APPS=["defender"],
        DEFENDER_REDIS_URL="redis://localhost:6379",
    )
    def test_urls_with_defender(self):
        """test_urls_with_defender

        Returns:

        """
        urlpatterns = get_auth_urls()
        self.assertTrue("admin/defender" in str(urlpatterns))
