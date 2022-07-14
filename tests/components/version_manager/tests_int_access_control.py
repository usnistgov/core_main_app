""" Access control testing
"""

from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerAccessControlFixtures,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

fixture_template_vm = TemplateVersionManagerAccessControlFixtures()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestVersionManagerDisable(MongoIntegrationBaseTestCase):
    """TestVersionManagerDisable"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_disable_user_version_manager_raises_access_control_error(self):
        """test anonymous disable user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)

    def test_anonymous_disable_global_version_manager_raises_access_control_error(self):
        """test anonymous disable global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.global_tvm, request=mock_request)

    def test_user_can_disable_user_version_manager(self):
        """test user can disable user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_user_disable_global_version_manager_raises_access_control_error(self):
        """test user disable global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.global_tvm, request=mock_request)

    def test_user_disable_other_user_version_manager_raises_access_control_error(self):
        """test user disable other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)

    def test_staff_can_disable_user_version_manager(self):
        """test staff can disable user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_staff_can_disable_global_version_manager(self):
        """test staff can disable global version manager

        Returns:

        """
        self.fixture.global_tvm.is_disabled = False
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable(self.fixture.global_tvm, request=mock_request)
        self.assertTrue(self.fixture.global_tvm.is_disabled)

    def test_staff_disable_other_user_version_manager_raises_access_control_error(self):
        """test staff disable other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)

    def test_superuser_can_disable_user_version_manager(self):
        """test superuser can disable user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_superuser_can_disable_global_version_manager(self):
        """test superuser can disable global version manager

        Returns:

        """
        self.fixture.global_tvm.is_disabled = False
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.global_tvm, request=mock_request)
        self.assertTrue(self.fixture.global_tvm.is_disabled)

    def test_superuser_can_disable_other_user_version_manager(self):
        """test superuser can disable other user version manager

        Returns:

        """
        self.fixture.user2_tvm.is_disabled = False
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)
        self.assertTrue(self.fixture.user2_tvm.is_disabled)


class TestVersionManagerRestore(MongoIntegrationBaseTestCase):
    """TestVersionManagerRestore"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_restore_user_version_manager_raises_access_control_error(self):
        """test anonymous restore user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)

    def test_anonymous_restore_global_version_manager_raises_access_control_error(self):
        """test anonymous restore global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.global_tvm, request=mock_request)

    def test_user_can_restore_user_version_manager(self):
        """test user can restore user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_user_restore_global_version_manager_raises_access_control_error(self):
        """test user restore global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.global_tvm, request=mock_request)

    def test_user_restore_other_user_version_manager_raises_access_control_error(self):
        """test user restore other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)

    def test_staff_can_restore_user_version_manager(self):
        """test staff can restore user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_staff_can_restore_global_version_manager(self):
        """test staff can restore global version manager

        Returns:

        """
        self.fixture.global_tvm.is_disabled = True
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore(self.fixture.global_tvm, request=mock_request)
        self.assertFalse(self.fixture.global_tvm.is_disabled)

    def test_staff_restore_other_user_version_manager_raises_access_control_error(self):
        """test staff restore other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)

    def test_superuser_can_restore_user_version_manager(self):
        """test superuser can restore user version manager

        Returns:

        """
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_superuser_can_restore_global_version_manager(self):
        """test superuser can restore global version manager

        Returns:

        """
        self.fixture.global_tvm.is_disabled = True
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.global_tvm, request=mock_request)
        self.assertFalse(self.fixture.global_tvm.is_disabled)

    def test_superuser_can_restore_other_user_version_manager(self):
        """test superuser can restore other user version manager

        Returns:

        """
        self.fixture.user2_tvm.is_disabled = True
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)
        self.assertFalse(self.fixture.user2_tvm.is_disabled)


class TestVersionManagerRestoreVersion(MongoIntegrationBaseTestCase):
    """TestVersionManagerRestoreVersion"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_restore_version_user_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous restore version user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_restore_version_global_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous restore version global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_restore_version_user_version_manager(self):
        """test user can restore version user version manager

        Returns:

        """
        self.fixture.user1_template.is_disabled = True
        self.fixture.user1_template.save_template()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            not in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_user_restore_version_global_version_manager_raises_access_control_error(
        self,
    ):
        """test user restore version global version manager raises access control error

        Returns:

        """
        self.fixture.global_template.is_disabled = True
        self.fixture.global_template.save_template()
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_restore_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test user restore version other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_restore_version_user_version_manager(self):
        """test staff can restore version user version manager

        Returns:

        """
        self.fixture.user1_template.is_disabled = True
        self.fixture.user1_template.save_template()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            not in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_staff_can_restore_version_global_version_manager(self):
        """test staff can restore version global version manager

        Returns:

        """
        self.fixture.global_template.is_disabled = True
        self.fixture.global_template.save_template()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            not in self.fixture.global_template.version_manager.disabled_versions
        )

    def test_staff_restore_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test staff restore version other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_restore_version_user_version_manager(self):
        """test superuser can restore version user version manager

        Returns:

        """
        self.fixture.user1_template.is_disabled = True
        self.fixture.user1_template.save_template()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            not in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_superuser_can_restore_version_global_version_manager(self):
        """test superuser can restore version global version manager

        Returns:

        """
        self.fixture.global_template.is_disabled = True
        self.fixture.global_template.save_template()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            not in self.fixture.global_template.version_manager.disabled_versions
        )

    def test_superuser_can_restore_version_other_user_version_manager(self):
        """test superuser can restore version other user version manager

        Returns:

        """
        self.fixture.user2_template.is_disabled = True
        self.fixture.user2_template.save_template()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore_version(
            self.fixture.user2_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user2_template.id)
            not in self.fixture.user2_template.version_manager.disabled_versions
        )


class TestVersionManagerDisableVersion(MongoIntegrationBaseTestCase):
    """TestVersionManagerDisableVersion"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_disable_version_user_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous disable version user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_disable_version_global_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous disable version global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_disable_version_user_version_manager(self):
        """test user can disable version user version manager

        Returns:

        """
        self.fixture.user1_template.is_current = False
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_user_disable_version_global_version_manager_raises_access_control_error(
        self,
    ):
        """test user disable version global version manager raises access control error

        Returns:

        """
        self.fixture.global_template.is_current = False
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_disable_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test user disable version other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_disable_version_user_version_manager(self):
        """test staff can disable version user version manager

        Returns:

        """
        self.fixture.user1_template.is_current = False
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_staff_can_disable_version_global_version_manager(self):
        """test staff can disable version global version manager

        Returns:

        """
        self.fixture.global_template.is_current = False
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            in self.fixture.global_template.version_manager.disabled_versions
        )

    def test_staff_disable_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test staff disable version other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_disable_version_user_version_manager(self):
        """test superuser can disable version user version manager

        Returns:

        """
        self.fixture.user1_template.is_current = False
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id)
            in self.fixture.user1_template.version_manager.disabled_versions
        )

    def test_superuser_can_disable_version_global_version_manager(self):
        """test superuser can disable version global version manager

        Returns:

        """
        self.fixture.global_template.is_current = False
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            in self.fixture.global_template.version_manager.disabled_versions
        )

    def test_superuser_can_disable_version_other_user_version_manager(self):
        """test superuser can disable version other user version manager

        Returns:

        """
        self.fixture.user2_template.is_current = False
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable_version(
            self.fixture.user2_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user2_template.id)
            in self.fixture.user2_template.version_manager.disabled_versions
        )


class TestVersionManagerSetCurrent(MongoIntegrationBaseTestCase):
    """TestVersionManagerSetCurrent"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_set_current_user_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous set current user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_set_current_global_version_manager_raises_access_control_error(
        self,
    ):
        """test anonymous set current global version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_set_current_user_version_manager(self):
        """test user can set current user version manager

        Returns:

        """
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.user1_template.id),
            self.fixture.user1_template.version_manager.current,
        )

    def test_user_set_current_global_version_manager_raises_access_control_error(self):
        """test user set current global version manager raises access control error

        Returns:

        """
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.global_template, request=mock_request
            )

    def test_user_set_current_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test user set current other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_set_current_user_version_manager(self):
        """test staff can set current user version manager

        Returns:

        """
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.user1_template.id),
            self.fixture.user1_template.version_manager.current,
        )

    def test_staff_can_set_current_global_version_manager(self):
        """test staff can set current global version manager

        Returns:

        """
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.set_current(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.global_template.id),
            self.fixture.global_template.version_manager.current,
        )

    def test_staff_set_current_other_user_version_manager_raises_access_control_error(
        self,
    ):
        """test staff set current other user version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_set_current_user_version_manager(self):
        """test superuser can set current user version manager

        Returns:

        """
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.user1_template.id),
            self.fixture.user1_template.version_manager.current,
        )

    def test_superuser_can_set_current_global_version_manager(self):
        """test superuser can set current global version manager

        Returns:

        """
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.set_current(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.global_template.id),
            self.fixture.global_template.version_manager.current,
        )

    def test_superuser_can_set_current_other_user_version_manager(self):
        """test superuser can set current other user version manager

        Returns:

        """
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.set_current(
            self.fixture.user2_template, request=mock_request
        )
        self.assertEqual(
            str(self.fixture.user2_template.id),
            self.fixture.user2_template.version_manager.current,
        )


class TestVersionManagerUpsert(MongoIntegrationBaseTestCase):
    """TestVersionManagerUpsert"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_upsert_user_version_manager_as_anonymous_raises_access_control_error(self):
        """test upsert user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test upsert global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_user_saves(self):
        """test upsert own version manager as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_user_raises_access_control_error(
        self,
    ):
        """test upsert other users version manager as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_user_raises_access_control_error(self):
        """test upsert global version manager as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_staff_saves(self):
        """test upsert own version manager as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test upsert other users version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_staff_saves(self):
        """test upsert global version manager as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_superuser_saves(self):
        """test upsert own version manager as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_superuser_saves(self):
        """test upsert other users version manager as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_superuser_saves(self):
        """test upsert global version manager as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)


class TestVersionManagerGetVersionNumber(MongoIntegrationBaseTestCase):
    """TestVersionManagerGetVersionNumber"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_version_number_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get version number user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_number(
                self.fixture.user1_tvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    def test_get_version_number_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get version number global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_number(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_get_version_number_own_version_manager_as_user_returns_version_number(
        self,
    ):
        """test get version number own version manager as user returns version number

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_number = version_manager_api.get_version_number(
            self.fixture.user1_tvm, self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(version_number, 1)

    def test_global_version_manager_as_user_returns_version_number(self):
        """test global version manager as user returns version number

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_number = version_manager_api.get_version_number(
            self.fixture.global_tvm,
            self.fixture.global_template.id,
            request=mock_request,
        )
        self.assertEqual(version_number, 1)

    def test_get_version_number_other_users_version_manager_raises_access_control_error(
        self,
    ):
        """test get version number other users version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_number(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_get_version_number_any_version_manager_as_superuser_returns_version_number(
        self,
    ):
        """test get version number any version manager as superuser returns version number

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_number = version_manager_api.get_version_number(
            self.fixture.user1_tvm, self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(version_number, 1)
        version_number = version_manager_api.get_version_number(
            self.fixture.user2_tvm, self.fixture.user2_template.id, request=mock_request
        )
        self.assertEqual(version_number, 1)
        version_number = version_manager_api.get_version_number(
            self.fixture.global_tvm,
            self.fixture.global_template.id,
            request=mock_request,
        )
        self.assertEqual(version_number, 1)

    def test_get_version_number_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get version number other users version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_number(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )


class TestVersionManagerGetVersionByNumber(MongoIntegrationBaseTestCase):
    """TestVersionManagerGetVersionByNumber"""

    fixture = fixture_template_vm

    def setUp(self):
        """setup

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_version_by_number_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get version by number user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user1_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_global_version_manager_as_anonymous_raises_acl_error(
        self,
    ):
        """test get version by number global version manager as anonymous raises acl error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.global_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_own_version_manager_as_user_returns_version(self):
        """test get version by number own version manager as user returns version

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version = version_manager_api.get_version_by_number(
            self.fixture.user1_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.user1_template.id))

    def test_global_version_manager_as_user_returns_version(self):
        """test global version manager as user returns version

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version = version_manager_api.get_version_by_number(
            self.fixture.global_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.global_template.id))

    def test_get_version_by_number_other_users_version_manager_raises_access_control_error(
        self,
    ):
        """test get version by number other users version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user2_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_any_version_manager_as_superuser_returns_version(
        self,
    ):
        """test get version by number any version manager as superuser returns version

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version = version_manager_api.get_version_by_number(
            self.fixture.user1_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.user1_template.id))
        version = version_manager_api.get_version_by_number(
            self.fixture.user2_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.user2_template.id))
        version = version_manager_api.get_version_by_number(
            self.fixture.global_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.global_template.id))

    def test_get_version_by_number_other_users_version_manager_as_staff_raises_acl_error(
        self,
    ):
        """test get version by number other users version manager as staff raises acl error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user2_tvm, 1, request=mock_request
            )
