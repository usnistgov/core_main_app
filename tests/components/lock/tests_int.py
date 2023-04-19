""" Int Test Lock
"""

from core_main_app.commons.exceptions import LockError
from core_main_app.utils.tests_tools.MockUser import create_mock_user

from tests.components.data.fixtures.fixtures import DataFixtures
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.components.lock import api as lock_api


fixture_data = DataFixtures()


class TestLockIsObjectLocked(IntegrationBaseTestCase):
    """Test Lock Is Object Locked"""

    fixture = fixture_data
    user1 = create_mock_user("1")
    user2 = create_mock_user("2")

    def test_is_object_locked_returns_true_when_locked(self):
        """test is object locked returns true when locked

        Returns:

        """
        # Arrange
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Act
        result = lock_api.is_object_locked(self.fixture.data_1, self.user2)

        # Assert
        self.assertEqual(result, True)

    def test_is_object_locked_returns_false_when_unlocked(self):
        """test is object locked returns false when unlocked

        Returns:

        """

        # Act
        result = lock_api.is_object_locked(self.fixture.data_1, self.user1)

        # Assert
        self.assertEqual(result, False)


class TestLockSetLock(IntegrationBaseTestCase):
    """Test Set Lock"""

    fixture = fixture_data
    user1 = create_mock_user("1")
    user2 = create_mock_user("2")

    def test_set_lock_locks_object_when_object_is_unlocked(self):
        """test set lock locks object when object is unlocked

        Returns:

        """

        # Act
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Assert
        self.assertEqual(
            lock_api.is_object_locked(self.fixture.data_1, self.user2), True
        )

    def test_set_lock_keeps_object_locked(self):
        """test set lock keeps object locked

        Returns:

        """
        # Arrange
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Act
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Assert
        self.assertEqual(
            lock_api.is_object_locked(self.fixture.data_1, self.user2), True
        )

    def test_set_lock_on_object_already_locked_by_another_user_raises_lock_error(
        self,
    ):
        """test set lock on object already locked by another user raises lock error

        Returns:

        """
        # Arrange
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Act  # Assert
        with self.assertRaises(LockError):
            lock_api.set_lock_object(self.fixture.data_1, self.user2)


class TestLockRemoveLockOnObject(IntegrationBaseTestCase):
    """Test Remove Lock On Object"""

    fixture = fixture_data
    user1 = create_mock_user("1")
    user2 = create_mock_user("2")

    def test_remove_lock_unlocks_object_when_locked(self):
        """test remove lock unlocks object when locked

        Returns:

        """
        # Arrange
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Act
        lock_api.remove_lock_on_object(self.fixture.data_1, self.user1)

        # Assert
        self.assertEqual(
            lock_api.is_object_locked(self.fixture.data_1, self.user2), False
        )

    def test_remove_lock_keeps_object_unlocked(self):
        """test set lock keeps object locked

        Returns:

        """
        # Act
        lock_api.remove_lock_on_object(self.fixture.data_1, self.user1)

        # Assert
        self.assertEqual(
            lock_api.is_object_locked(self.fixture.data_1, self.user2), False
        )

    def test_remove_lock_different_user_keeps_object_locked(self):
        """test set lock different user keeps object locked

        Returns:

        """
        # Arrange
        lock_api.set_lock_object(self.fixture.data_1, self.user1)

        # Act
        lock_api.remove_lock_on_object(self.fixture.data_1, self.user2)

        # Assert
        self.assertEqual(
            lock_api.is_object_locked(self.fixture.data_1, self.user2), True
        )
