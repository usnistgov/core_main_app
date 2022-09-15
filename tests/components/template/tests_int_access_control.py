""" Access control testing
"""

from tests.components.template.fixtures.fixtures import AccessControlTemplateFixture

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template import api as template_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

fixture_template = AccessControlTemplateFixture()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestTemplateUpsert(MongoIntegrationBaseTestCase):
    """TestTemplateUpsert"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_upsert_user_template_as_anonymous_raises_access_control_error(self):
        """test upsert user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_global_template_as_anonymous_raises_access_control_error(self):
        """test upsert global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_user_saves(self):
        """test upsert own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_user_raises_access_control_error(self):
        """test upsert other users template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_user_raises_access_control_error(self):
        """test upsert global template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_staff_saves(self):
        """test upsert own template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_staff_raises_access_control_error(self):
        """test upsert other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_staff_saves(self):
        """test upsert global template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_superuser_saves(self):
        """test upsert own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_superuser_saves(self):
        """test upsert other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_superuser_saves(self):
        """test upsert global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.global_template, request=mock_request)


class TestTemplateSetDisplayName(MongoIntegrationBaseTestCase):
    """TestTemplateSetDisplayName"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_set_display_name_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test set display name user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user1_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        """test set display name global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.global_template, "new_name", request=mock_request
            )

    def test_set_display_name_own_template_as_user_saves(self):
        """test set display name own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        """test set display name other users template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user2_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_user_raises_access_control_error(self):
        """test set display name global template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.global_template, "new_name", request=mock_request
            )

    def test_set_display_name_own_template_as_staff_saves(self):
        """test set display name own template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        """test set display name other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user2_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_staff_saves(self):
        """test set display name global template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.set_display_name(
            self.fixture.global_template, "new_name", request=mock_request
        )

    def test_set_display_name_own_template_as_superuser_saves(self):
        """test set display name own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_superuser_saves(self):
        """test set display name other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.user2_template, "new_name", request=mock_request
        )

    def test_set_display_name_global_template_as_superuser_saves(self):
        """test set display name global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.global_template, "new_name", request=mock_request
        )


class TestTemplateGet(MongoIntegrationBaseTestCase):
    """TestTemplateGet"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_template_as_anonymous_raises_access_control_error(self):
        """test get user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.get_by_id(self.fixture.user1_template.id, request=mock_request)

    def test_get_global_template_as_anonymous_raises_access_control_error(self):
        """test get global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.get_by_id(
                self.fixture.global_template.id, request=mock_request
            )

    def test_get_own_template_as_user_returns_template(self):
        """test get own template as user returns template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template = template_api.get_by_id(
            self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user1_template)

    def test_global_template_as_user_returns_template(self):
        """test global template as user returns template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template = template_api.get_by_id(
            self.fixture.global_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.global_template)

    def test_get_other_users_template_raises_access_control_error(self):
        """test get other users template raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.get_by_id(self.fixture.user2_template.id, request=mock_request)

    def test_get_any_template_as_superuser_returns_template(self):
        """test get any template as superuser returns template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template = template_api.get_by_id(
            self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user1_template)
        template = template_api.get_by_id(
            self.fixture.user2_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user2_template)
        template = template_api.get_by_id(
            self.fixture.global_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.global_template)

    def test_get_other_users_template_as_staff_raises_access_control_error(self):
        """test get other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.get_by_id(self.fixture.user2_template.id, request=mock_request)


class TestTemplateGetAllAccessibleByIdList(MongoIntegrationBaseTestCase):
    """TestTemplateGetAllAccessibleByIdList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()
        self.template_id_list = [
            str(self.fixture.user1_template.id),
            str(self.fixture.user2_template.id),
            str(self.fixture.global_template.id),
        ]

    def test_get_all_accessible_by_id_list_as_anonymous_returns_nothing(self):
        """test get all accessible by id list as anonymous returns nothing

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_id_list_as_user_returns_accessible_templates(self):
        """test get all accessible by id list as user returns accessible templates

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_id_list_as_staff_returns_accessible_templates(self):
        """test get all accessible by id list as staff returns accessible templates

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_id_list_as_superuser_returns_accessible_templates(
        self,
    ):
        """test get all accessible by id list as superuser returns accessible templates

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))


class TestTemplateGetAllByHash(MongoIntegrationBaseTestCase):
    """TestTemplateGetAllByHash"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_accessible_by_hash_as_anonymous_does_not_return_user_template(
        self,
    ):
        """test get all accessible by hash as anonymous does not return user template

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_anonymous_does_not_return_global(self):
        """test get all accessible by hash as anonymous does not return global

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_user_returns_user_template(self):
        """test get all accessible by hash as user returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_user_returns_global_template(self):
        """test get all accessible by hash as user returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_as_user_does_not_return_other_user_template(
        self,
    ):
        """test get all accessible by hash as user does not return other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_staff_returns_user_template(self):
        """test get all accessible by hash as staff returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_staff_returns_global_template(self):
        """test get all accessible by hash as staff returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_as_staff_does_not_return_other_user_template(
        self,
    ):
        """test get all accessible by hash as staff does not return other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_user_template(self):
        """test get all accessible by hash as superuser returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_global_template(self):
        """test get all accessible by hash as superuser returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_other_user_template(self):
        """test get all accessible by hash as superuser returns other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))


class TestTemplateGetAllByHashList(MongoIntegrationBaseTestCase):
    """TestTemplateGetAllByHashList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_accessible_by_hash_list_as_anonymous_does_not_return_user_template(
        self,
    ):
        """test get all accessible by hash list as anonymous does not return user template

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_anonymous_does_not_return_global(self):
        """test get all accessible by hash list as anonymous does not return global

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.global_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_user_returns_user_template(self):
        """test get all accessible by hash list as user returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_user_returns_global_template(self):
        """test get all accessible by hash list as user returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.global_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_list_as_user_does_not_return_other_user_template(
        self,
    ):
        """test get all accessible by hash list as user does not return other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_staff_returns_user_template(self):
        """test get all accessible by hash list as staff returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_staff_returns_global_template(self):
        """test get all accessible by hash list as staff returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.global_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_list_as_staff_does_not_return_other_user_template(
        self,
    ):
        """test get all accessible by hash list as staff does not return other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_superuser_returns_user_template(self):
        """test get all accessible by hash list as superuser returns user template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_superuser_returns_global_template(self):
        """test get all accessible by hash list as superuser returns global template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.global_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_list_as_superuser_returns_other_user_template(
        self,
    ):
        """test get all accessible by hash list as superuser returns other user template

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))


class TestTemplateGetAll(MongoIntegrationBaseTestCase):
    """TestTemplateGetAll"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user = create_mock_user(user_id="1")
        self.staff_user = create_mock_user(user_id="2", is_staff=True)
        self.superuser = create_mock_user(user_id="3", is_superuser=True)
        self.fixture.insert_data()
        self.template_id_list = [
            str(self.fixture.user1_template.id),
            str(self.fixture.user2_template.id),
            str(self.fixture.global_template.id),
        ]

    def test_get_all_as_anonymous_returns_empty_list(self):
        """test get all as anonymous returns empty list

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all(request=mock_request)
        self.assertEqual(templates.count(), 0)

    def test_get_all_as_user_returns_accessible_templates(self):
        """test get all as user returns accessible templates

        Returns:

        """
        mock_request = create_mock_request(user=self.user)
        templates = template_api.get_all(request=mock_request)
        self.assertEqual(templates.count(), 2)
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_as_staff_returns_accessible_templates(self):
        """test get all as staff returns accessible templates

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user)
        templates = template_api.get_all(request=mock_request)
        self.assertEqual(templates.count(), 2)
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_as_superuser_returns_all_templates(self):
        """test get all as superuser returns all templates

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser)
        templates = template_api.get_all(request=mock_request)
        self.assertEqual(templates.count(), 3)
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))


class TestTemplateDelete(MongoIntegrationBaseTestCase):
    """TestTemplateDelete"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_delete_user_template_as_anonymous_raises_access_control_error(self):
        """test delete user template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_global_template_as_anonymous_raises_access_control_error(self):
        """test delete global template as anonymous raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_user_saves(self):
        """test delete own template as user saves

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_user_raises_access_control_error(self):
        """test delete other users template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_user_raises_access_control_error(self):
        """test delete global template as user raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_staff_saves(self):
        """test delete own template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_staff_raises_access_control_error(self):
        """test delete other users template as staff raises access control error

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_staff_saves(self):
        """test delete global template as staff saves

        Returns:

        """
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_superuser_saves(self):
        """test delete own template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_superuser_saves(self):
        """test delete other users template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_superuser_saves(self):
        """test delete global template as superuser saves

        Returns:

        """
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.global_template, request=mock_request)
