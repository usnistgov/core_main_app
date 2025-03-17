""" Unit tests for `core_main_app.utils.drf package`.
"""

from unittest import TestCase

from core_main_app.utils.drf.authentication import BearerTokenAuthentication


class TestBearerTokenAuthentication(TestCase):
    """Unit tests for `BearerTokenAuthentication` class."""

    def test_bearer_token_authentication_class_uses_bearer_keyword(self):
        bearer_token_class = BearerTokenAuthentication()
        self.assertEqual(bearer_token_class.keyword, "Bearer")
