""" Access control testing
"""

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template_version_manager import api as template_vm_api
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


class TestTemplateVersionManagerInsert(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_insert_user_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user1_tvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    def test_insert_global_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.insert(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.insert(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_staff_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.insert(
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )

    def test_insert_own_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user2_tvm, self.fixture.user2_template, request=mock_request
        )

    def test_insert_global_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )


class TestTemplateEditTitle(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_edit_title_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user1_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.global_tvm, "new_name", request=mock_request
            )

    def test_edit_title_own_template_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user2_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.global_tvm, "new_name", request=mock_request
            )

    def test_edit_title_own_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user2_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.edit_title(
            self.fixture.global_tvm, "new_name", request=mock_request
        )

    def test_edit_title_own_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.user2_tvm, "new_name", request=mock_request
        )

    def test_edit_title_global_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.global_tvm, "new_name", request=mock_request
        )


class TestTemplateGetGlobalVersionManagers(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_global_version_managers_as_anonymous_raises_acces_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_global_version_managers(request=mock_request)

    def test_get_global_version_managers_as_user_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_staff_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_superuser_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveGlobalVersionManager(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_global_version_manager_as_anonymous_raises_acces_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_active_global_version_manager(request=mock_request)

    def test_get_active_global_version_manager_as_user_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_staff_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_superuser_returns_global_tvm(self):
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveVersionManagerByUserId(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_version_manager_by_user_id_as_anonymous_returns_nothing(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        self.assertEqual(list_tvm.count(), 0)

    def test_get_active_version_manager_by_user_id_as_user_returns_user_templates(self):
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.user1.id))

    def test_get_active_version_manager_by_user_id_as_staff_returns_user_templates(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.staff_user1.id))

    def test_get_active_version_manager_by_user_id_as_superuser_returns_user_templates(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.superuser1.id))


class TestTemplateVersionManagerGetByVersionId(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_by_version_id_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_version_id(
                str(self.fixture.user1_template.id), request=mock_request
            )

    def test_get_by_version_id_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_version_id(
                str(self.fixture.global_template.id), request=mock_request
            )

    def test_get_by_version_id_own_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.get_by_version_id(
            str(self.fixture.user1_template.id), request=mock_request
        )

    def test_get_by_version_id_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_version_id(
                str(self.fixture.user2_template.id), request=mock_request
            )

    def test_get_by_version_id_global_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.get_by_version_id(
            str(self.fixture.global_template.id), request=mock_request
        )

    def test_get_by_version_id_own_template_as_staff_returns_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.get_by_version_id(
            str(self.fixture.user1_template.id), request=mock_request
        )

    def test_get_by_version_id_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_version_id(
                str(self.fixture.user2_template.id), request=mock_request
            )

    def test_get_by_version_id_global_template_as_staff_returns_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.get_by_version_id(
            str(self.fixture.global_template.id), request=mock_request
        )

    def test_get_by_version_id_own_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_by_version_id(
            str(self.fixture.user1_template.id), request=mock_request
        )

    def test_get_by_version_id_other_users_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_by_version_id(
            str(self.fixture.user2_template.id), request=mock_request
        )

    def test_get_by_version_id_global_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_by_version_id(
            str(self.fixture.global_template.id), request=mock_request
        )


class TestTemplateVersionManagerGetAllByVersionIds(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_by_version_ids_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_all_by_version_ids(
                [str(self.fixture.user1_template.id)], request=mock_request
            )

    def test_get_all_by_version_ids_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_all_by_version_ids(
                [str(self.fixture.global_template.id)], request=mock_request
            )

    def test_get_all_by_version_ids_own_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.user1_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_all_by_version_ids(
                [str(self.fixture.user2_template.id)], request=mock_request
            )

    def test_get_all_by_version_ids_global_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.global_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_own_template_as_staff_returns_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.user1_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_all_by_version_ids(
                [str(self.fixture.user2_template.id)], request=mock_request
            )

    def test_get_all_by_version_ids_global_template_as_staff_returns_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.global_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_own_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.user1_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_other_users_template_as_superuser_returns_template(
        self,
    ):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.user2_template.id)], request=mock_request
        )

    def test_get_all_by_version_ids_global_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.get_all_by_version_ids(
            [str(self.fixture.global_template.id)], request=mock_request
        )


class TestTemplateGetAllByUserId(MongoIntegrationBaseTestCase):

    fixture = fixture_template_vm

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_by_user_id_as_anonymous_returns_nothing(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        self.assertEqual(list_tvm.count(), 0)

    def test_get_all_by_user_id_as_user_returns_user_templates(self):
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.user1.id))

    def test_get_all_by_user_id_as_staff_returns_user_templates(self):
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.staff_user1.id))

    def test_get_all_by_user_id_as_superuser_returns_user_templates(self):
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.superuser1.id))
