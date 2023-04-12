""" Urls test class
"""
from unittest import TestCase

from django.test import override_settings

from core_main_app.utils.urls import get_auth_urls


class TestUrls(TestCase):
    """TestUrls"""

    @override_settings(ENABLE_SAML2_SSO_AUTH=True)
    def test_urls_with_ENABLE_SAML2_SSO_AUTH(self):
        """test_urls_with_ENABLE_SAML2_SSO_AUTH

        Returns:

        """
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))
        self.assertTrue("saml2" in str(urlpatterns))

    @override_settings(ENABLE_SAML2_SSO_AUTH=False)
    def test_urls(self):
        """test_urls

        Returns:

        """
        urlpatterns = get_auth_urls()
        self.assertTrue("core_main_app_login" in str(urlpatterns))
