""" Access control testing
"""

from django.test import override_settings

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template_version_manager import (
    api as template_vm_api,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_main_app.components.template_version_manager import access_control

from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerAccessControlFixtures,
    TemplateVersionManagerOrderingFixtures,
)


fixture_template_vm = TemplateVersionManagerAccessControlFixtures()
fixture_template_vm_ordering = TemplateVersionManagerOrderingFixtures()


class TestTemplateVersionManagerGet(IntegrationBaseTestCase):
    """TestTemplateVersionManagerGet"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(
                self.fixture.user1_tvm.id, request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_user_version_manager_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test get user version manager as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(
                self.fixture.user1_tvm.id, request=mock_request
            )

    def test_get_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(
                self.fixture.global_tvm.id, request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_global_version_manager_as_anonymous_with_access_right_returns_global_template(
        self,
    ):
        """test get global version manager as anonymous with access right returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        version_manager = template_vm_api.get_by_id(
            self.fixture.global_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_own_version_manager_as_user_returns_version_manager(self):
        """test get own version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = template_vm_api.get_by_id(
            self.fixture.user1_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)

    def test_global_version_manager_as_user_returns_version_manager(self):
        """test global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = template_vm_api.get_by_id(
            self.fixture.global_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_raises_access_control_error(self):
        """test get other users version manager raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(
                self.fixture.user2_tvm.id, request=mock_request
            )

    def test_get_any_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get any version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = template_vm_api.get_by_id(
            self.fixture.user1_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user1_tvm)
        version_manager = template_vm_api.get_by_id(
            self.fixture.user2_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.user2_tvm)
        version_manager = template_vm_api.get_by_id(
            self.fixture.global_tvm.id, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_other_users_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get other users version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(
                self.fixture.user2_tvm.id, request=mock_request
            )


class TestTemplateVersionManagerGetByIdList(IntegrationBaseTestCase):
    """TesTemplateVersionManagerGetByIdList"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_by_id_list_user_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get by id list user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id_list(
                [str(self.fixture.user1_tvm.id)], request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_by_id_list_user_version_manager_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test get by id list user version manager as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id_list(
                [str(self.fixture.user1_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get by id list global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id_list(
                [str(self.fixture.global_tvm.id)], request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_by_id_list_global_version_manager_as_anonymous_with_access_right_returns_version_manager(
        self,
    ):
        """test get by id list global version manager as anonymous with access right version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_user_version_manager_as_user_returns_version_manager(
        self,
    ):
        """test get by id list user version manager as user returns template version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_user_returns_version_manager(
        self,
    ):
        """test get by id list global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_user_raises_access_control_error(
        self,
    ):
        """test get by id list other user version manager as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id_list(
                [str(self.fixture.user2_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_user_version_manager_as_staff_returns_version_manager(
        self,
    ):
        """test get by id list user version manager as staff returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_staff_returns_version_manager(
        self,
    ):
        """test get by id list global version manager as staff returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_staff_raises_access_control_error(
        self,
    ):
        """test get by id list other user version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id_list(
                [str(self.fixture.user2_tvm.id)], request=mock_request
            )

    def test_get_by_id_list_user_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get by id list user version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.user1_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))

    def test_get_by_id_list_global_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get by id list global version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.global_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm not in list(version_managers))
        self.assertTrue(self.fixture.global_tvm in list(version_managers))

    def test_get_by_id_list_other_user_version_manager_as_superuser_returns_version_manager(
        self,
    ):
        """test get by id list other user version manager as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_managers = template_vm_api.get_by_id_list(
            [str(self.fixture.user2_tvm.id)], request=mock_request
        )
        self.assertTrue(self.fixture.user1_tvm not in list(version_managers))
        self.assertTrue(self.fixture.user2_tvm in list(version_managers))
        self.assertTrue(self.fixture.global_tvm not in list(version_managers))


class TestTemplateVersionManagerGetActiveGlobalVersionManagerByTitle(
    IntegrationBaseTestCase
):
    """TestTemplateVersionManagerGetActiveGlobalVersionManagerByTitle"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_global_version_manager_by_title_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get active global version manager by title as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_active_global_version_manager_by_title_as_anonymous_with_access_right_returns_version_manager(
        self,
    ):
        """test get active global version manager by title as anonymous with access right returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        version_manager = (
            template_vm_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_as_user_returns_version_manager(
        self,
    ):
        """test get active global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = (
            template_vm_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_superuser_returns_version_manager(
        self,
    ):
        """test get active global version manager by title as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = (
            template_vm_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_staff_raises_access_control_error(
        self,
    ):
        """test get active global version manager by title as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = (
            template_vm_api.get_active_global_version_manager_by_title(
                self.fixture.global_tvm.title, request=mock_request
            )
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)


class TestTemplateVersionManagerInsert(IntegrationBaseTestCase):
    """TestTemplateVersionManagerInsert"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_insert_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test insert user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user1_tvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_insert_user_template_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test insert user template as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user1_tvm,
                self.fixture.user1_template,
                request=mock_request,
            )

    def test_insert_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test insert global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_insert_global_template_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test insert global template as anonymous with access right raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_user_saves(self):
        """test insert own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.insert(
            self.fixture.user1_tvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        """test insert other users template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_user_raises_access_control_error(self):
        """test insert global template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.global_tvm,
                self.fixture.global_template,
                request=mock_request,
            )

    def test_insert_own_template_as_staff_saves(self):
        """test insert own template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.insert(
            self.fixture.user1_tvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        """test insert other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.insert(
                self.fixture.user2_tvm,
                self.fixture.user2_template,
                request=mock_request,
            )

    def test_insert_global_template_as_staff_saves(self):
        """test insert global template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_template,
            request=mock_request,
        )

    def test_insert_own_template_as_superuser_saves(self):
        """test insert own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user1_tvm,
            self.fixture.user1_template,
            request=mock_request,
        )

    def test_insert_other_users_template_as_superuser_saves(self):
        """test insert other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user2_tvm,
            self.fixture.user2_template,
            request=mock_request,
        )

    def test_insert_global_template_as_superuser_saves(self):
        """test insert global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.global_tvm,
            self.fixture.global_template,
            request=mock_request,
        )


class TestTemplateEditTitle(IntegrationBaseTestCase):
    """TestTemplateEditTitle"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_edit_title_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test edit title user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user1_tvm, "new_name", request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_edit_title_user_template_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test edit title user template as anonymous with access right  raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user1_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test edit title global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.global_tvm, "new_name", request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_edit_title_global_template_as_anonymous_with_access_right_raises_access_control_error(
        self,
    ):
        """test edit title global template as anonymous with access right  raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.global_tvm, "new_name", request=mock_request
            )

    def test_edit_title_own_template_as_user_saves(self):
        """test edit title own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        """test edit title other users template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user2_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_user_raises_access_control_error(
        self,
    ):
        """test edit title global template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.global_tvm, "new_name", request=mock_request
            )

    def test_edit_title_own_template_as_staff_saves(self):
        """test edit title own template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        """test edit title other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.edit_title(
                self.fixture.user2_tvm, "new_name", request=mock_request
            )

    def test_edit_title_global_template_as_staff_saves(self):
        """test edit title global template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_vm_api.edit_title(
            self.fixture.global_tvm, "new_name", request=mock_request
        )

    def test_edit_title_own_template_as_superuser_saves(self):
        """test edit title own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.user1_tvm, "new_name", request=mock_request
        )

    def test_edit_title_other_users_template_as_superuser_saves(self):
        """test edit title other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.user2_tvm, "new_name", request=mock_request
        )

    def test_edit_title_global_template_as_superuser_saves(self):
        """test edit title global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.edit_title(
            self.fixture.global_tvm, "new_name", request=mock_request
        )


class TestTemplateGetGlobalVersionManagers(IntegrationBaseTestCase):
    """TestTemplateGetGlobalVersionManagers"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_global_version_managers_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get global version managers as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_global_version_managers(request=mock_request)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_global_version_managers_as_anonymous_with_access_right_returns_global_tvm(
        self,
    ):
        """test get global version managers as anonymous with access right returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_user_returns_global_tvm(self):
        """test get global version managers as user returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_staff_returns_global_tvm(self):
        """test get global version managers as staff returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_superuser_returns_global_tvm(self):
        """test get global version managers as superuser returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_global_version_managers(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveGlobalVersionManager(IntegrationBaseTestCase):
    """TestTemplateGetActiveGlobalVersionManager"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_global_version_manager_as_anonymous_raises_access_control_error(
        self,
    ):
        """test get active global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_active_global_version_manager(
                request=mock_request
            )

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_active_global_version_manager_as_anonymous_with_access_right_returns_global_tvm(
        self,
    ):
        """test get active global version manager as anonymous with access right returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_user_returns_global_tvm(
        self,
    ):
        """test get active global version manager as user returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_staff_returns_global_tvm(
        self,
    ):
        """test get active global version manager as staff returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_superuser_returns_global_tvm(
        self,
    ):
        """test get active global version manager as superuser returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveVersionManagerByUserId(IntegrationBaseTestCase):
    """TestTemplateGetActiveVersionManagerByUserId"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_active_version_manager_by_user_id_as_anonymous_returns_nothing(
        self,
    ):
        """test get active version manager by user id as anonymous returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        self.assertEqual(list_tvm.count(), 0)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_active_version_manager_by_user_id_as_anonymous_with_access_right_returns_nothing(
        self,
    ):
        """test get active version manager by user id as anonymous with access right returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        self.assertEqual(list_tvm.count(), 0)

    def test_get_active_version_manager_by_user_id_as_user_returns_user_templates(
        self,
    ):
        """test get active version manager by user id as user returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.user1.id))

    def test_get_active_version_manager_by_user_id_as_staff_returns_user_templates(
        self,
    ):
        """test get active version manager by user id as staff returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.staff_user1.id))

    def test_get_active_version_manager_by_user_id_as_superuser_returns_user_templates(
        self,
    ):
        """test get active version manager by user id as superuser returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.superuser1.id))


class TestTemplateGetAllByUserId(IntegrationBaseTestCase):
    """TestTemplateGetAllByUserId"""

    fixture = fixture_template_vm

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_by_user_id_as_anonymous_returns_nothing(self):
        """test get all by user id as anonymous returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        self.assertEqual(list_tvm.count(), 0)

    @override_settings(CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT=True)
    def test_get_all_by_user_id_as_anonymous_with_access_right_returns_nothing(
        self,
    ):
        """test get all by user id as anonymous with access right returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        self.assertEqual(list_tvm.count(), 0)

    def test_get_all_by_user_id_as_user_returns_user_templates(self):
        """test get all by user id as user returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.user1.id))

    def test_get_all_by_user_id_as_staff_returns_user_templates(self):
        """test get all by user id as staff returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.staff_user1.id))

    def test_get_all_by_user_id_as_superuser_returns_user_templates(self):
        """test get all by user id as superuser returns user templates

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_all_by_user_id(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, str(self.superuser1.id))


class TestUpdateTemplatesOrdering(IntegrationBaseTestCase):
    """Test Update Templates Ordering"""

    fixture = fixture_template_vm_ordering

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_update_user_templates_ordering_as_anonymous_raises_access_control_error(
        self,
    ):
        """test update user templates ordering as anonymous raises acl error

        Returns:x

        """

        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id, self.fixture.tvm1.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api._update_template_version_manager_ordering(
                list_templates_ordering,
                create_mock_request(user=self.anonymous_user),
            )

    def test_update_global_templates_ordering_as_anonymous_raises_access_control_error(
        self,
    ):
        """test update global templates ordering as anonymous raises access control error

        Returns:

        """
        # Arrange
        list_templates_ordering = [
            self.fixture.global_tvm2.id,
            self.fixture.global_tvm1.id,
        ]
        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api._update_template_version_manager_ordering(
                list_templates_ordering,
                create_mock_request(user=self.anonymous_user),
            )

    def test_update_own_templates_ordering_as_user_saves(self):
        """test update own templates ordering as user saves

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id, self.fixture.tvm1.id]
        # Act
        template_vm_api._update_template_version_manager_ordering(
            list_templates_ordering, create_mock_request(user=self.user1)
        )

    def test_update_other_users_template_ordering_as_user_raises_access_control_error(
        self,
    ):
        """test update other users template ordering as user raises access control error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id, self.fixture.tvm1.id]
        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api._update_template_version_manager_ordering(
                list_templates_ordering, create_mock_request(user=self.user2)
            )

    def test_update_other_users_template_ordering_as_superuser_saves(self):
        """test update other users template ordering as superuser saves

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id, self.fixture.tvm1.id]
        # Act
        template_vm_api._update_template_version_manager_ordering(
            list_templates_ordering, create_mock_request(user=self.superuser1)
        )

    def test_update_global_template_ordering_as_superuser_saves(self):
        """test update other users template ordering as superuser saves

        Returns:

        """
        # Arrange
        list_templates_ordering = [
            self.fixture.global_tvm2.id,
            self.fixture.global_tvm1.id,
        ]
        # Act
        template_vm_api._update_template_version_manager_ordering(
            list_templates_ordering, create_mock_request(user=self.superuser1)
        )


class TestAccessControlCanWriteList(IntegrationBaseTestCase):
    """Test Access Control Can Write List"""

    fixture = fixture_template_vm_ordering

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.staff_user1 = create_mock_user(user_id="3", is_staff=True)
        self.superuser1 = create_mock_user(user_id="4", is_superuser=True)
        self.fixture.insert_data()

    def test_access_control_can_write_list_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_access_control_can_write_list_as_anonymous_raises_access_control_error"""

        # Arrange
        template_vm_list = [self.fixture.tvm2.id, self.fixture.tvm1.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control.can_write_list(
                template_vm_api._update_template_version_manager_ordering,
                template_vm_list,
                create_mock_request(user=self.anonymous_user),
            )

    def test_access_control_can_write_list_as_owner_returns_function(self):
        """test_access_control_can_write_list_as_owner_returns_function"""

        # Arrange
        template_vm_list = [self.fixture.tvm2.id, self.fixture.tvm1.id]

        # Act
        access_control.can_write_list(
            template_vm_api._update_template_version_manager_ordering,
            template_vm_list,
            create_mock_request(user=self.user1),
        )

    def test_access_control_can_write_list_user_templates_as_user_raises_access_control_error(
        self,
    ):
        """test_access_control_can_write_list_user_templates_as_user_raises_access_control_error"""
        # Arrange
        template_vm_list = [self.fixture.tvm2.id, self.fixture.tvm1.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control.can_write_list(
                template_vm_api._update_template_version_manager_ordering,
                template_vm_list,
                create_mock_request(user=self.user2),
            )

    def test_access_control_can_write_list_global_templates_as_user_raises_access_control_error(
        self,
    ):
        """test_access_control_can_write_list_global_templates_as_user_raises_access_control_error"""
        # Arrange
        template_vm_list = [
            self.fixture.global_tvm2.id,
            self.fixture.global_tvm1.id,
        ]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control.can_write_list(
                template_vm_api._update_template_version_manager_ordering,
                template_vm_list,
                create_mock_request(user=self.user2),
            )

    def test_access_control_can_write_list_user_templates_as_staff_raises_access_control_error(
        self,
    ):
        """test_access_control_can_write_list_user_templates_as_staff_raises_access_control_error"""

        # Arrange
        template_vm_list = [self.fixture.tvm2.id, self.fixture.tvm1.id]

        # Act
        with self.assertRaises(AccessControlError):
            access_control.can_write_list(
                template_vm_api._update_template_version_manager_ordering,
                template_vm_list,
                create_mock_request(user=self.staff_user1),
            )

    def test_access_control_can_write_list_global_templates_as_staff_returns_function(
        self,
    ):
        """test_access_control_can_write_list_global_templates_as_staff_returns_functiong"""

        # Arrange
        template_vm_list = [
            self.fixture.global_tvm1.id,
            self.fixture.global_tvm2.id,
        ]

        # Act
        access_control.can_write_list(
            template_vm_api._update_template_version_manager_ordering,
            template_vm_list,
            create_mock_request(user=self.staff_user1),
        )

    def test_access_control_can_write_list_as_superuser_returns_function(self):
        """test_access_control_can_write_list_as_superuser_returns_function"""

        # Arrange
        template_vm_list = [self.fixture.global_tvm2.id, self.fixture.tvm1.id]

        # Act
        access_control.can_write_list(
            template_vm_api._update_template_version_manager_ordering,
            template_vm_list,
            create_mock_request(user=self.superuser1),
        )


class TestUpdateUserTemplateOrdering(IntegrationBaseTestCase):
    """Test Update User Template Ordering"""

    fixture = fixture_template_vm_ordering

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.user2 = create_mock_user(user_id="2")
        self.superuser1 = create_mock_user(user_id="3", is_superuser=True)
        self.fixture.insert_data()

    def test_update_user_template_ordering_as_owner_updates_templates(
        self,
    ):
        """test_update_user_template_ordering_as_owner_updates_templates

        Returns:

        """
        # Arrange
        template_vm_list = [self.fixture.tvm1.id]

        template_vm_api.update_user_template_ordering(
            template_vm_list, create_mock_request(user=self.user1)
        )

    def test_update_user_template_ordering_as_user_raises_acl_error(
        self,
    ):
        """test_update_user_template_ordering_as_user_raises_acl_error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_user_template_ordering(
                list_templates_ordering, create_mock_request(user=self.user2)
            )

    def test_update_user_template_ordering_as_anonymous_raises_acl_error(
        self,
    ):
        """test_update_user_template_ordering_as_anonymous_raises_acl_error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_user_template_ordering(
                list_templates_ordering,
                create_mock_request(user=self.anonymous_user),
            )

    def test_update_user_template_ordering_as_superuser_raises_acl_error(
        self,
    ):
        """test_update_user_template_ordering_as_superuser_raises_acl_error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.tvm2.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_user_template_ordering(
                list_templates_ordering,
                create_mock_request(user=self.superuser1),
            )


class TestUpdateGlobalTemplateOrdering(IntegrationBaseTestCase):
    "Test Update Global Template Ordering"

    fixture = fixture_template_vm_ordering

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.superuser1 = create_mock_user(
            user_id="3", is_superuser=True, is_staff=True
        )
        self.fixture.insert_data()

    def test_update_global_template_ordering_as_superuser_updates_templates(
        self,
    ):
        """test_update_global_template_ordering_as_superuser_updates_templates

        Returns:

        """
        # Arrange
        template_vm_list = [self.fixture.global_tvm1.id]

        template_vm_api.update_global_template_ordering(
            template_vm_list, request=create_mock_request(user=self.superuser1)
        )

    def test_update_user_template_ordering_as_superuser_raises_acl_error(
        self,
    ):
        """test_update_user_template_ordering_as_superuser_raises_acl_error

        Returns:

        """
        # Arrange
        template_vm_list = [self.fixture.tvm2.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_global_template_ordering(
                template_vm_list,
                request=create_mock_request(user=self.superuser1),
            )

    def test_update_global_template_ordering_as_user_raises_acl_error(
        self,
    ):
        """test_update_global_template_ordering_as_user_raises_acl_error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.global_tvm1.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_global_template_ordering(
                list_templates_ordering,
                request=create_mock_request(user=self.user1),
            )

    def test_update_user_template_ordering_as_anonymous_raises_acl_error(
        self,
    ):
        """test_update_user_template_ordering_as_anonymous_raises_acl_error

        Returns:

        """
        # Arrange
        list_templates_ordering = [self.fixture.global_tvm1.id]

        # Act # Assert
        with self.assertRaises(AccessControlError):
            template_vm_api.update_global_template_ordering(
                list_templates_ordering,
                request=create_mock_request(user=self.anonymous_user),
            )
