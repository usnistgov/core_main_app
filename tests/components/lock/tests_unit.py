""" Unit tests for Lock components
"""
from unittest import TestCase

from unittest.mock import Mock

from core_main_app.commons.exceptions import LockError
from core_main_app.components.lock.api import _check_object_locked
from core_main_app.settings import LOCK_OBJECT_TTL
from core_main_app.utils.datetime import datetime_now, datetime_timedelta
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCheckObjectLocked(TestCase):
    """Test _check_object_locked function"""

    def setUp(self) -> None:
        self.mock_object = Mock()
        self.mock_user = create_mock_user(user_id=1)
        self.mock_lock = Mock()

    def test_get_object_locked_fails_returns_false(self):
        """test_get_object_locked_fails_returns_false"""
        self.mock_lock.get_object_locked.side_effect = Exception(
            "mock_get_object_locked_exception"
        )

        result = _check_object_locked(
            self.mock_object, self.mock_user, self.mock_lock
        )
        self.assertFalse(result)

    def test_object_lock_expired_returns_false(self):
        """test_object_lock_expired_returns_false"""
        mock_lock_object = Mock()
        mock_lock_object.lock_date = datetime_now() - datetime_timedelta(
            seconds=10 * LOCK_OBJECT_TTL
        )
        self.mock_lock.get_object_locked.return_value = mock_lock_object

        result = _check_object_locked(
            self.mock_object, self.mock_user, self.mock_lock
        )
        self.assertFalse(result)

    def test_user_is_object_owner_returns_true(self):
        """test_user_is_object_owner_returns_true"""
        mock_lock_object = Mock()
        mock_lock_object.lock_date = datetime_now()
        mock_lock_object.user_id = str(self.mock_user.id)
        self.mock_lock.get_object_locked.return_value = mock_lock_object

        result = _check_object_locked(
            self.mock_object, self.mock_user, self.mock_lock
        )
        self.assertTrue(result)

    def test_user_not_owner_raises_error(self):
        """test_user_not_owner_raises_error"""
        mock_lock_object = Mock()
        mock_lock_object.lock_date = datetime_now()
        mock_lock_object.user_id = "2"
        self.mock_lock.get_object_locked.return_value = mock_lock_object

        with self.assertRaises(LockError):
            _check_object_locked(
                self.mock_object, self.mock_user, self.mock_lock
            )
