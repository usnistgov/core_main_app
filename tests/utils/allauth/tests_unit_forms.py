""" Allauth Adapter utils test class
"""

from unittest import TestCase
from unittest.mock import MagicMock

from django.test import override_settings

from core_main_app.utils.allauth.forms import (
    get_core_signup_form_base_class,
    CoreSignupForm,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_website_app.views.user.forms import RequestAccountForm


class TestGetCoreSignupFormBaseClass(TestCase):
    """TestGetCoreSignupFormBaseClass"""

    def test_get_core_signup_form_base_class(
        self,
    ):
        """test_get_core_signup_form_base_class

        Returns:

        """
        base_class = get_core_signup_form_base_class()
        self.assertTrue(base_class == RequestAccountForm)

    @override_settings(INSTALLED_APPS=[])
    def test_get_core_signup_form_base_class_is_none_if_missing_installed_apps(
        self,
    ):
        """test_get_core_signup_form_base_class_is_none_if_missing_installed_apps

        Returns:

        """
        base_class = get_core_signup_form_base_class()
        self.assertIsNone(base_class)


class TestCoreSignupFormClass(TestCase):
    """TestGetCoreSignupFormBaseClass"""

    def test_core_signup_form_signup_method(
        self,
    ):
        """test_get_core_signup_form_base_class

        Returns:

        """
        mock_request = MagicMock()
        mock_user = create_mock_user("1")
        core_signup_form = CoreSignupForm()
        result = core_signup_form.signup(request=mock_request, user=mock_user)
        self.assertIsNone(result)
