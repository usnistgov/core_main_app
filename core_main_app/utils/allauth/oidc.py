""" Utils for allauth oidc configuration
"""

import os


def load_allauth_oidc_conf_from_env():
    return {
        # Optional PKCE defaults to False, but may be required by your provider
        # Applies to all APPS.
        "OAUTH_PKCE_ENABLED": os.getenv(
            "OIDC_OAUTH_PKCE_ENABLED", "False"
        ).lower()
        == "true",
        "APPS": [
            {
                "provider_id": os.getenv("OIDC_PROVIDER_ID"),
                "name": os.getenv("OIDC_PROVIDER_NAME"),
                "client_id": os.getenv("OIDC_CLIENT_ID"),
                "secret": os.getenv("OIDC_CLIENT_SECRET"),
                "settings": {
                    "server_url": os.getenv("OIDC_SERVER_URL"),
                },
            },
        ],
    }
