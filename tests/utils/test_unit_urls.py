""" Urls test class
"""

from unittest import TestCase

from django.test import override_settings

from core_main_app.utils.urls import get_auth_urls


class TestUrls(TestCase):
    """TestUrls"""

    @override_settings(ENABLE_SAML2_SSO_AUTH=True)
    def test_urls_with_enable_saml2_sso_auth(self):
        """test_urls_with_enable_saml2_sso_auth

        Returns:

        """
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))
        self.assertTrue("saml2" in str(urlpatterns))

    @override_settings(ENABLE_SAML2_SSO_AUTH=False)
    def test_urls_without_enable_saml2_sso_auth(self):
        """test_urls_without_enable_saml2_sso_auth

        Returns:

        """
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))

    @override_settings(ENABLE_ALLAUTH=True)
    def test_urls_with_enable_allauth(self):
        """test_urls_with_enable_allauth

        Returns:

        """
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
