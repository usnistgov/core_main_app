""" Access control testing
"""

from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerAccessControlFixtures,
)

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template_version_manager import api as template_vm_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

fixture_template_vm = TemplateVersionManagerAccessControlFixtures()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestTemplateVersionManagerGet(MongoIntegrationBaseTestCase):
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

    def test_get_user_version_manager_as_anonymous_raises_access_control_error(self):
        """test get user version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(self.fixture.user1_tvm.id, request=mock_request)

    def test_get_global_version_manager_as_anonymous_raises_access_control_error(self):
        """test get global version manager as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(self.fixture.global_tvm.id, request=mock_request)

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
            template_vm_api.get_by_id(self.fixture.user2_tvm.id, request=mock_request)

    def test_get_any_version_manager_as_superuser_returns_version_manager(self):
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

    def test_get_other_users_version_manager_as_staff_raises_access_control_error(self):
        """test get other users version manager as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_by_id(self.fixture.user2_tvm.id, request=mock_request)


class TesTemplateVersionManagerGetByIdList(MongoIntegrationBaseTestCase):
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

    def test_get_by_id_list_user_version_manager_as_user_returns_version_version_manager(
        self,
    ):
        """test get by id list user version manager as user returns version version manager

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

    def test_get_by_id_list_user_version_manager_as_staff_returns_version_manager(self):
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
    MongoIntegrationBaseTestCase
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

    def test_get_active_global_version_manager_as_user_returns_version_manager(self):
        """test get active global version manager as user returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        version_manager = template_vm_api.get_active_global_version_manager_by_title(
            self.fixture.global_tvm.title, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_superuser_returns_version_manager(
        self,
    ):
        """test get active global version manager by title as superuser returns version manager

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        version_manager = template_vm_api.get_active_global_version_manager_by_title(
            self.fixture.global_tvm.title, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)

    def test_get_active_global_version_manager_by_title_as_staff_raises_access_control_error(
        self,
    ):
        """test get active global version manager by title as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        version_manager = template_vm_api.get_active_global_version_manager_by_title(
            self.fixture.global_tvm.title, request=mock_request
        )
        self.assertEqual(version_manager, self.fixture.global_tvm)


class TestTemplateVersionManagerInsert(MongoIntegrationBaseTestCase):
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

    def test_insert_user_template_as_anonymous_raises_access_control_error(self):
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

    def test_insert_global_template_as_anonymous_raises_access_control_error(self):
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

    def test_insert_own_template_as_user_saves(self):
        """test insert own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_vm_api.insert(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_user_raises_access_control_error(self):
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
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_staff_raises_access_control_error(self):
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
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )

    def test_insert_own_template_as_superuser_saves(self):
        """test insert own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user1_tvm, self.fixture.user1_template, request=mock_request
        )

    def test_insert_other_users_template_as_superuser_saves(self):
        """test insert other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.user2_tvm, self.fixture.user2_template, request=mock_request
        )

    def test_insert_global_template_as_superuser_saves(self):
        """test insert global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_vm_api.insert(
            self.fixture.global_tvm, self.fixture.global_template, request=mock_request
        )


class TestTemplateEditTitle(MongoIntegrationBaseTestCase):
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

    def test_edit_title_global_template_as_user_raises_access_control_error(self):
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


class TestTemplateGetGlobalVersionManagers(MongoIntegrationBaseTestCase):
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

    def test_get_global_version_managers_as_anonymous_raises_acces_control_error(self):
        """test get global version managers as anonymous raises acces control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_global_version_managers(request=mock_request)

    def test_get_global_version_managers_as_user_returns_global_tvm(self):
        """test get global version managers as user returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_staff_returns_global_tvm(self):
        """test get global version managers as staff returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_global_version_managers_as_superuser_returns_global_tvm(self):
        """test get global version managers as superuser returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_global_version_managers(request=mock_request)
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveGlobalVersionManager(MongoIntegrationBaseTestCase):
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

    def test_get_active_global_version_manager_as_anonymous_raises_acces_control_error(
        self,
    ):
        """test get active global version manager as anonymous raises acces control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_vm_api.get_active_global_version_manager(request=mock_request)

    def test_get_active_global_version_manager_as_user_returns_global_tvm(self):
        """test get active global version manager as user returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_staff_returns_global_tvm(self):
        """test get active global version manager as staff returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)

    def test_get_active_global_version_manager_as_superuser_returns_global_tvm(self):
        """test get active global version manager as superuser returns global tvm

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        list_tvm = template_vm_api.get_active_global_version_manager(
            request=mock_request
        )
        for tvm in list_tvm:
            self.assertEqual(tvm.user, None)


class TestTemplateGetActiveVersionManagerByUserId(MongoIntegrationBaseTestCase):
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

    def test_get_active_version_manager_by_user_id_as_anonymous_returns_nothing(self):
        """test get active version manager by user id as anonymous returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        list_tvm = template_vm_api.get_active_version_manager_by_user_id(
            request=mock_request
        )
        self.assertEqual(list_tvm.count(), 0)

    def test_get_active_version_manager_by_user_id_as_user_returns_user_templates(self):
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


class TestTemplateGetAllByUserId(MongoIntegrationBaseTestCase):
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
