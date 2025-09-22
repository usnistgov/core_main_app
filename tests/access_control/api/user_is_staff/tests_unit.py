""" Unit tests for `core_main_app.access_control.api.user_is_staff`.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from core_main_app.access_control import api as access_control_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestUserIsStaff(TestCase):
    """Unit tests for the `user_is_staff` function"""

    def setUp(self):
        """setUp"""
        self.staff_user = create_mock_user(1, is_staff=True)
        self.non_staff_user = create_mock_user(1, is_staff=False)

        self.mock_func = MagicMock()
        self.mock_args = []
        self.mock_kwargs = {}

    def test_user_retrieved_from_args(self):
        """test_user_retrieved_from_args"""
        self.mock_args = [None, self.staff_user]

        access_control_api.user_is_staff(
            self.mock_func, *self.mock_args, **self.mock_kwargs
        )
        self.mock_func.assert_called()

    def test_user_not_in_args_retrieved_from_kwargs(self):
        """test_user_not_in_args_retrieved_from_kwargs"""
        self.mock_kwargs = {"arg001": None, "user": self.staff_user}

        access_control_api.user_is_staff(
            self.mock_func, *self.mock_args, **self.mock_kwargs
        )
        self.mock_func.assert_called()

    def test_user_not_present_raise_access_control_error(self):
        """test_user_not_present_raise_access_control_error"""
        with self.assertRaises(AccessControlError):
            access_control_api.user_is_staff(
                self.mock_func, *self.mock_args, **self.mock_kwargs
            )

    def test_user_not_staff_in_args_raise_access_control_error(self):
        """test_user_not_staff_in_args_raise_access_control_error"""
        self.mock_args = [None, self.non_staff_user]

        with self.assertRaises(AccessControlError):
            access_control_api.user_is_staff(
                self.mock_func, *self.mock_args, **self.mock_kwargs
            )

    def test_user_not_staff_in_kwargs_raise_access_control_error(self):
        """test_user_not_staff_in_kwargs_raise_access_control_error"""
        self.mock_kwargs = {"arg001": None, "user": self.non_staff_user}

        with self.assertRaises(AccessControlError):
            access_control_api.user_is_staff(
                self.mock_func, *self.mock_args, **self.mock_kwargs
            )
