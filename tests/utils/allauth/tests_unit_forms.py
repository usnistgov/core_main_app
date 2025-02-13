""" Allauth Adapter utils test class
"""

from unittest import TestCase
from unittest.mock import MagicMock

from core_main_app.utils.allauth.forms import (
    CoreAccountSignupForm,
    CoreSocialAccountSignupForm,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCoreAccountSignupFormClass(TestCase):
    """TestCoreAccountSignupFormClass"""

    def test_core_signup_form_signup_method(
        self,
    ):
        """test_core_signup_form_signup_method

        Returns:

        """
        mock_request = MagicMock()
        mock_user = create_mock_user("1")
        core_signup_form = CoreAccountSignupForm()
        result = core_signup_form.signup(request=mock_request, user=mock_user)
        self.assertIsNone(result)


class TestCoreSocialAccountSignupFormClass(TestCase):
    """TestCoreSocialAccountSignupFormClass"""

    def test_core_signup_form_signup_method(
        self,
    ):
        """test_core_signup_form_signup_method

        Returns:

        """
        mock_request = MagicMock()
        mock_user = create_mock_user("1")
        core_signup_form = CoreSocialAccountSignupForm(sociallogin=MagicMock())
        result = core_signup_form.signup(request=mock_request, user=mock_user)
        self.assertIsNone(result)
