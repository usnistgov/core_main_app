""" Access control testing
"""

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerAccessControlFixtures,
)

fixture_template_vm = TemplateVersionManagerAccessControlFixtures()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestVersionManagerGet(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_version_manager_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get(self.fixture.user1_tvm.id, request=mock_request)

    def test_get_global_version_manager_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get(self.fixture.global_tvm.id, request=mock_request)

    def test_get_own_version_manager_as_user_returns_version_manager(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.get(
            self.fixture.user1_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)

    def test_global_version_manager_as_user_returns_version_manager(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.get(
            self.fixture.global_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get(self.fixture.user2_tvm.id, request=mock_request)

    def test_get_any_version_manager_as_superuser_returns_version_manager(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.get(
            self.fixture.user1_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)
        version_manager = version_manager_api.get(
            self.fixture.user2_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user2_tvm)
        version_manager = version_manager_api.get(
            self.fixture.global_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_as_staff_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get(self.fixture.user2_tvm.id, request=mock_request)


class TestVersionManagerGetByIdList(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_by_id_list_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_by_id_list(
                [str(self.fixture.user1_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_by_id_list(
                [str(self.fixture.global_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_user_version_manager_as_user_returns_version_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_user_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_by_id_list(
                [str(self.fixture.user2_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_user_version_manager_as_staff_returns_version_manager(self):
        mock_request = create_mock_request(user=self.staff_user1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_staff_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_by_id_list(
                [str(self.fixture.user2_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_user_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = version_manager_api.get_by_id_list(
            [str(self.fixture.user2_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))


class TestVersionManagerGetFromVersion(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_version_manager_from_version_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_from_version(
                self.fixture.user1_template, request=mock_request
            )

    def test_get_global_version_manager_from_version_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_from_version(
                self.fixture.global_template, request=mock_request
            )

    def test_get_own_version_manager_from_version_as_user_returns_version_manager(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.get_from_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)

    def test_global_version_manager_from_version_as_user_returns_version_manager(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.get_from_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_from_version_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_from_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_get_any_version_manager_from_version_as_superuser_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.get_from_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)
        version_manager = version_manager_api.get_from_version(
            self.fixture.user2_template, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user2_tvm)
        version_manager = version_manager_api.get_from_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_from_version_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_from_version(
                self.fixture.user2_template, request=mock_request
            )


class TestVersionManagerDisable(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_disable_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)

    def test_anonymous_disable_global_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.global_tvm, request=mock_request)

    def test_user_can_disable_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_user_disable_global_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.global_tvm, request=mock_request)

    def test_user_disable_other_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)

    def test_staff_can_disable_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_staff_can_disable_global_version_manager(self):
        self.fixture.global_tvm.is_disabled = False
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.disable(self.fixture.global_tvm, request=mock_request)
        self.assertTrue(self.fixture.global_tvm.is_disabled)

    def test_staff_disable_other_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)

    def test_superuser_can_disable_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = False
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.user1_tvm, request=mock_request)
        self.assertTrue(self.fixture.user1_tvm.is_disabled)

    def test_superuser_can_disable_global_version_manager(self):
        self.fixture.global_tvm.is_disabled = False
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.global_tvm, request=mock_request)
        self.assertTrue(self.fixture.global_tvm.is_disabled)

    def test_superuser_can_disable_other_user_version_manager(self):
        self.fixture.user2_tvm.is_disabled = False
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.disable(self.fixture.user2_tvm, request=mock_request)
        self.assertTrue(self.fixture.user2_tvm.is_disabled)


class TestVersionManagerRestore(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_restore_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)

    def test_anonymous_restore_global_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.global_tvm, request=mock_request)

    def test_user_can_restore_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_user_restore_global_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.global_tvm, request=mock_request)

    def test_user_restore_other_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)

    def test_staff_can_restore_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_staff_can_restore_global_version_manager(self):
        self.fixture.global_tvm.is_disabled = True
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.restore(self.fixture.global_tvm, request=mock_request)
        self.assertFalse(self.fixture.global_tvm.is_disabled)

    def test_staff_restore_other_user_version_manager_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)

    def test_superuser_can_restore_user_version_manager(self):
        self.fixture.user1_tvm.is_disabled = True
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.user1_tvm, request=mock_request)
        self.assertFalse(self.fixture.user1_tvm.is_disabled)

    def test_superuser_can_restore_global_version_manager(self):
        self.fixture.global_tvm.is_disabled = True
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.global_tvm, request=mock_request)
        self.assertFalse(self.fixture.global_tvm.is_disabled)

    def test_superuser_can_restore_other_user_version_manager(self):
        self.fixture.user2_tvm.is_disabled = True
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.restore(self.fixture.user2_tvm, request=mock_request)
        self.assertFalse(self.fixture.user2_tvm.is_disabled)


class TestVersionManagerRestoreVersion(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_restore_version_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_restore_version_global_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_restore_version_user_version_manager(self):
        self.fixture.user1_tvm.disabled_versions = [str(self.fixture.user1_template.id)]
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) not in version_manager.disabled_versions
        )

    def test_user_restore_version_global_version_manager_raises_access_control_error(
        self,
    ):
        self.fixture.global_tvm.disabled_versions = [
            str(self.fixture.global_template.id)
        ]
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_restore_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_restore_version_user_version_manager(self):
        self.fixture.user1_tvm.disabled_versions = [str(self.fixture.user1_template.id)]
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) not in version_manager.disabled_versions
        )

    def test_staff_can_restore_version_global_version_manager(self):
        self.fixture.global_tvm.disabled_versions = [
            str(self.fixture.global_template.id)
        ]
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.restore_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            not in version_manager.disabled_versions
        )

    def test_staff_restore_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.restore_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_restore_version_user_version_manager(self):
        self.fixture.user1_tvm.disabled_versions = [str(self.fixture.user1_template.id)]
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.restore_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) not in version_manager.disabled_versions
        )

    def test_superuser_can_restore_version_global_version_manager(self):
        self.fixture.global_tvm.disabled_versions = [
            str(self.fixture.global_template.id)
        ]
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.restore_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id)
            not in version_manager.disabled_versions
        )

    def test_superuser_can_restore_version_other_user_version_manager(self):
        self.fixture.user2_tvm.disabled_versions = [str(self.fixture.user2_template.id)]
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.restore_version(
            self.fixture.user2_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user2_template.id) not in version_manager.disabled_versions
        )


class TestVersionManagerDisableVersion(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_disable_version_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_disable_version_global_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_disable_version_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) in version_manager.disabled_versions
        )

    def test_user_disable_version_global_version_manager_raises_access_control_error(
        self,
    ):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.global_template, request=mock_request
            )

    def test_user_disable_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_disable_version_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) in version_manager.disabled_versions
        )

    def test_staff_can_disable_version_global_version_manager(self):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.disable_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id) in version_manager.disabled_versions
        )

    def test_staff_disable_version_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.disable_version(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_disable_version_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.disable_version(
            self.fixture.user1_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user1_template.id) in version_manager.disabled_versions
        )

    def test_superuser_can_disable_version_global_version_manager(self):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.disable_version(
            self.fixture.global_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.global_template.id) in version_manager.disabled_versions
        )

    def test_superuser_can_disable_version_other_user_version_manager(self):
        self.fixture.user2_tvm.current = "current_id"
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.disable_version(
            self.fixture.user2_template, request=mock_request
        )
        self.assertTrue(
            str(self.fixture.user2_template.id) in version_manager.disabled_versions
        )


class TestVersionManagerSetCurrent(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_anonymous_set_current_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user1_template, request=mock_request
            )

    def test_anonymous_set_current_global_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.global_template, request=mock_request
            )

    def test_user_can_set_current_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        version_manager = version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.user1_template.id), version_manager.current)

    def test_user_set_current_global_version_manager_raises_access_control_error(self):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.global_template, request=mock_request
            )

    def test_user_set_current_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user2_template, request=mock_request
            )

    def test_staff_can_set_current_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.user1_template.id), version_manager.current)

    def test_staff_can_set_current_global_version_manager(self):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = version_manager_api.set_current(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.global_template.id), version_manager.current)

    def test_staff_set_current_other_user_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.set_current(
                self.fixture.user2_template, request=mock_request
            )

    def test_superuser_can_set_current_user_version_manager(self):
        self.fixture.user1_tvm.current = "current_id"
        self.fixture.user1_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.set_current(
            self.fixture.user1_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.user1_template.id), version_manager.current)

    def test_superuser_can_set_current_global_version_manager(self):
        self.fixture.global_tvm.current = "current_id"
        self.fixture.global_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.set_current(
            self.fixture.global_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.global_template.id), version_manager.current)

    def test_superuser_can_set_current_other_user_version_manager(self):
        self.fixture.user2_tvm.current = "current_id"
        self.fixture.user2_tvm.save()
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = version_manager_api.set_current(
            self.fixture.user2_template, request=mock_request
        )
        self.assertEqual(str(self.fixture.user2_template.id), version_manager.current)


class TestVersionManagerUpsert(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_upsert_user_version_manager_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)

    def test_upsert_own_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.user1_tvm, request=mock_request)

    def test_upsert_other_users_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.user2_tvm, request=mock_request)

    def test_upsert_global_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.upsert(self.fixture.global_tvm, request=mock_request)


class TestVersionManagerInsertVersion(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_insert_version_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.insert_version(
                self.fixture.user1_tvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    def test_insert_version_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.insert_version(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_version_own_version_manager_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager_api.insert_version(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_version_other_users_version_manager_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.insert_version(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_version_global_version_manager_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.insert_version(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_version_own_version_manager_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.insert_version(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_version_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.insert_version(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_version_global_version_manager_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager_api.insert_version(
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )

    def test_insert_version_own_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.insert_version(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_version_other_users_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.insert_version(
            self.fixture.user2_tvm, self.fixture.user2_template, request=mock_request
        )

    def test_insert_version_global_version_manager_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager_api.insert_version(
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )


class TestVersionManagerGetActiveGlobalVersionManagerByTitle(
    MongoIntegrationBaseTestCase
):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_global_version_manager_by_title_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )

    def test_get_active_global_version_manager_as_user_returns_version_manager(self):
        mock_request = create_mock_request(user=self.user1)
        version_manager = (
            version_manager_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_superuser_returns_version_manager(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = (
            version_manager_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = (
            version_manager_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)


class TestVersionManagerGetVersionNumber(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_version_number_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
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
        mock_request = create_mock_request(user=self.user1)
        version_number = version_manager_api.get_version_number(
            self.fixture.user1_tvm, self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(version_number, 1)

    def test_global_version_manager_as_user_returns_version_number(self):
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
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_number(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )


class TestVersionManagerGetVersionByNumber(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_version_by_number_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user1_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.global_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_own_version_manager_as_user_returns_version(self):
        mock_request = create_mock_request(user=self.user1)
        version = version_manager_api.get_version_by_number(
            self.fixture.user1_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.user1_template.id))

    def test_global_version_manager_as_user_returns_version(self):
        mock_request = create_mock_request(user=self.user1)
        version = version_manager_api.get_version_by_number(
            self.fixture.global_tvm, 1, request=mock_request
        )
        self.assertEqual(version, str(self.fixture.global_template.id))

    def test_get_version_by_number_other_users_version_manager_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user2_tvm, 1, request=mock_request
            )

    def test_get_version_by_number_any_version_manager_as_superuser_returns_version(
        self,
    ):
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

    def test_get_version_by_number_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            version_manager_api.get_version_by_number(
                self.fixture.user2_tvm, 1, request=mock_request
            )
