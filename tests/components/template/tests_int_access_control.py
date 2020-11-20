""" Access control testing
"""

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template import api as template_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from tests.components.template.fixtures.fixtures import AccessControlTemplateFixture

fixture_template = AccessControlTemplateFixture()


# FIXME: missing tests where CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is True


class TestTemplateUpsert(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_upsert_user_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_global_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_staff_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.upsert(self.fixture.global_template, request=mock_request)

    def test_upsert_own_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.user1_template, request=mock_request)

    def test_upsert_other_users_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.user2_template, request=mock_request)

    def test_upsert_global_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.upsert(self.fixture.global_template, request=mock_request)


class TestTemplateSetDisplayName(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_set_display_name_user_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user1_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_anonymous_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.global_template, "new_name", request=mock_request
            )

    def test_set_display_name_own_template_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_user_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user2_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.global_template, "new_name", request=mock_request
            )

    def test_set_display_name_own_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_staff_raises_access_control_error(
        self,
    ):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.set_display_name(
                self.fixture.user2_template, "new_name", request=mock_request
            )

    def test_set_display_name_global_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.set_display_name(
            self.fixture.global_template, "new_name", request=mock_request
        )

    def test_set_display_name_own_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.user1_template, "new_name", request=mock_request
        )

    def test_set_display_name_other_users_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.user2_template, "new_name", request=mock_request
        )

    def test_set_display_name_global_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.set_display_name(
            self.fixture.global_template, "new_name", request=mock_request
        )


class TestTemplateGet(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_user_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.get(self.fixture.user1_template.id, request=mock_request)

    def test_get_global_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.get(self.fixture.global_template.id, request=mock_request)

    def test_get_own_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template = template_api.get(
            self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user1_template)

    def test_global_template_as_user_returns_template(self):
        mock_request = create_mock_request(user=self.user1)
        template = template_api.get(
            self.fixture.global_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.global_template)

    def test_get_other_users_template_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.get(self.fixture.user2_template.id, request=mock_request)

    def test_get_any_template_as_superuser_returns_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        template = template_api.get(
            self.fixture.user1_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user1_template)
        template = template_api.get(
            self.fixture.user2_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.user2_template)
        template = template_api.get(
            self.fixture.global_template.id, request=mock_request
        )
        self.assertEqual(template, self.fixture.global_template)

    def test_get_other_users_template_as_staff_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.get(self.fixture.user2_template.id, request=mock_request)


class TestTemplateGetAllAccessibleByIdList(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
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
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_id_list_as_user_returns_accessible_templates(self):
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_id_list_as_staff_returns_accessible_templates(self):
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
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_id_list(
            self.template_id_list, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))


class TestTemplateGetAllByHash(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_accessible_by_hash_as_anonymous_does_not_return_user_template(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_anonymous_does_not_return_global(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_user_returns_user_template(self):
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_user_returns_global_template(self):
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
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_as_staff_returns_user_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_staff_returns_global_template(self):
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
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_user_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user1_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_global_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.global_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))

    def test_get_all_accessible_by_hash_as_superuser_returns_other_user_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash(
            self.fixture.user2_template.hash, request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))


class TestTemplateGetAllByHashList(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_get_all_accessible_by_hash_list_as_anonymous_does_not_return_user_template(
        self,
    ):
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_anonymous_does_not_return_global(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.global_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_user_returns_user_template(self):
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_user_returns_global_template(self):
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
        mock_request = create_mock_request(user=self.user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(templates.count() == 0)

    def test_get_all_accessible_by_hash_list_as_staff_returns_user_template(self):
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_staff_returns_global_template(self):
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
        mock_request = create_mock_request(user=self.staff_user1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_superuser_returns_user_template(self):
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user1_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template not in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))

    def test_get_all_accessible_by_hash_list_as_superuser_returns_global_template(self):
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
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all_accessible_by_hash_list(
            [self.fixture.user2_template.hash], request=mock_request
        )
        self.assertTrue(self.fixture.user1_template not in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template not in list(templates))


class TestTemplateGetAll(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
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

    def test_get_all_as_anonymous_raises_acces_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.get_all(request=mock_request)

    def test_get_all_as_user_raises_acces_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.get_all(request=mock_request)

    def test_get_all_as_staff_raises_acces_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.get_all(request=mock_request)

    def test_get_all_as_superuser_returns_all_templates(self):
        mock_request = create_mock_request(user=self.superuser1)
        templates = template_api.get_all(request=mock_request)
        self.assertTrue(self.fixture.user1_template in list(templates))
        self.assertTrue(self.fixture.user2_template in list(templates))
        self.assertTrue(self.fixture.global_template in list(templates))


class TestTemplateDelete(MongoIntegrationBaseTestCase):

    fixture = fixture_template

    def setUp(self):
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.staff_user1 = create_mock_user(user_id="1", is_staff=True)
        self.superuser1 = create_mock_user(user_id="1", is_superuser=True)
        self.fixture.insert_data()

    def test_delete_user_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_global_template_as_anonymous_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.anonymous_user)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_user_saves(self):
        mock_request = create_mock_request(user=self.user1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_user_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_staff_raises_access_control_error(self):
        mock_request = create_mock_request(user=self.staff_user1)
        with self.assertRaises(AccessControlError):
            template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_staff_saves(self):
        mock_request = create_mock_request(user=self.staff_user1)
        template_api.delete(self.fixture.global_template, request=mock_request)

    def test_delete_own_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.user1_template, request=mock_request)

    def test_delete_other_users_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.user2_template, request=mock_request)

    def test_delete_global_template_as_superuser_saves(self):
        mock_request = create_mock_request(user=self.superuser1)
        template_api.delete(self.fixture.global_template, request=mock_request)
