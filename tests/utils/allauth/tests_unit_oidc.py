""" Allauth SAML utils test class
"""

import os
from unittest import TestCase

from core_main_app.utils.allauth.oidc import load_allauth_oidc_conf_from_env


class TestLoadAllauthOidcConfFromEnv(TestCase):
    """TestLoadAllauthOidcConfFromEnv"""

    def test_load_allauth_oidc_conf_from_env_returns_correct_conf(self):
        """test_load_allauth_oidc_conf_from_env_returns_correct_conf

        Returns:

        """
        os.environ["OIDC_PROVIDER_NAME"] = "Test Keycloak"
        os.environ["OIDC_PROVIDER_ID"] = "Keycloak"
        os.environ["OIDC_CLIENT_ID"] = "client_id"
        os.environ["OIDC_CLIENT_SECRET"] = "client_secret"
        os.environ["OIDC_SERVER_URL"] = (
            "http://localhost:8080/auth/realms/cdcs-realm"
        )
        self.assertEqual(
            {
                "APPS": [
                    {
                        "client_id": "client_id",
                        "name": "Test Keycloak",
                        "provider_id": "Keycloak",
                        "secret": "client_secret",
                        "settings": {
                            "server_url": "http://localhost:8080/auth/realms/cdcs-realm"
                        },
                    }
                ],
                "OAUTH_PKCE_ENABLED": False,
            },
            load_allauth_oidc_conf_from_env(),
        )
