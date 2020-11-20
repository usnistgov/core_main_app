""" Integration Test for Template Version Manager Rest API
"""
import json

from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager import api as vm_api
from core_main_app.rest.template_version_manager import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock, create_mock_request
from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerFixtures,
)

fixture_template = TemplateVersionManagerFixtures()


class TestGlobalTemplateVersionManagerList(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestGlobalTemplateVersionManagerList, self).setUp()

    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_global_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_returned_tvm_are_global(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.data[0]["user"], None)

    def test_get_filtered_by_correct_title_returns_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(),
            user,
            data={"title": self.fixture.template_vm_1.title},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_title_returns_no_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(),
            user,
            data={"title": "bad title"},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_filtered_by_expected_is_disabled_returns_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(),
            user,
            data={"is_disabled": self.fixture.template_vm_1.is_disabled},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_is_disabled_returns_no_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(),
            user,
            data={"is_disabled": not self.fixture.template_vm_1.is_disabled},
        )

        # Assert
        self.assertEqual(len(response.data), 0)


class TestUserTemplateVersionManagerList(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestUserTemplateVersionManagerList, self).setUp()

    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_user_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_returned_tvm_are_from_user(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.data[0]["user"], "1")

    def test_get_filtered_by_correct_title_returns_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(),
            user,
            data={"title": self.fixture.template_vm_2.title},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_title_returns_no_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(),
            user,
            data={"title": "bad title"},
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_filtered_by_expected_is_disabled_returns_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(),
            user,
            data={"is_disabled": self.fixture.template_vm_2.is_disabled},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_is_disabled_returns_no_tvm(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(),
            user,
            data={"is_disabled": not self.fixture.template_vm_2.is_disabled},
        )

        # Assert
        self.assertEqual(len(response.data), 0)


class TestTemplateVersionManagerDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestTemplateVersionManagerDetail, self).setUp()

    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            user,
            param={"pk": self.fixture.template_vm_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_tvm(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            user,
            param={"pk": self.fixture.template_vm_1.id},
        )

        # Assert
        self.assertEqual(response.data["title"], self.fixture.template_vm_1.title)

    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTemplateVersion(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestTemplateVersion, self).setUp()
        self.data = {
            "filename": "filename",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    def post_returns_http_201(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def post_to_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": str(self.fixture.template_vm_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def post_to_other_user_as_superuser_returns_http_201(self):
        # Arrange
        user = create_mock_user("2", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": str(self.fixture.template_vm_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_to_global_as_superuser_returns_http_201(self):
        # Arrange
        user = create_mock_user("2", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def post_to_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_post(
            views.TemplateVersion.as_view(),
            user,
            data=self.data,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserTemplateList(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestUserTemplateList, self).setUp()
        self.data = {
            "title": "title",
            "filename": "filename",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_owner_is_user(self):
        # Arrange
        user = create_mock_user("1")
        mock_request = create_mock_request(user=user)

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # get template version manager from posted template
        template_id = response.data["id"]
        template_object = template_api.get(template_id, request=mock_request)
        template_version_manager = vm_api.get_from_version(
            template_object, request=mock_request
        )

        # Assert
        self.assertEqual(template_version_manager.user, user.id)

    def test_post_template_name_already_exists_returns_http_400(self):
        # Arrange
        user = create_mock_user("1")
        self.data["title"] = self.fixture.template_vm_1.title

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_template_with_correct_dependency_returns_http_201(self):
        # Arrange
        user = create_mock_user("1")
        self.data["content"] = (
            "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:include schemaLocation='template1_1.xsd'/>"
            "<xs:element name='root'/></xs:schema>"
        )

        self.data["dependencies_dict"] = json.dumps(
            {"template1_1.xsd": str(self.fixture.template_1_1.id)}
        )

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        # FIXME: unable to download self dependency because server not running
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_download_url = reverse(
            "core_main_app_rest_template_download",
            kwargs={"pk": self.fixture.template_1_1.id},
        )
        self.assertTrue(expected_download_url in response.data["message"])

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_template_with_incorrect_dependency_schemaLocation_returns_http_400(
        self,
    ):
        # Arrange
        user = create_mock_user("1")
        self.data["content"] = (
            "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:include schemaLocation='template1_1.xsd'/>"
            "<xs:element name='root'/></xs:schema>"
        )

        self.data["dependencies_dict"] = json.dumps(
            {"test.xsd": str(self.fixture.template_1_1.id)}
        )

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_template_with_incorrect_dependency_id_returns_http_400(self):
        # Arrange
        user = create_mock_user("1")
        self.data["content"] = (
            "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:include schemaLocation='template1_1.xsd'/>"
            "<xs:element name='root'/></xs:schema>"
        )

        self.data["dependencies_dict"] = json.dumps({"template1_1.xsd": "bad_id"})

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGlobalTemplateList(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def setUp(self):
        super(TestGlobalTemplateList, self).setUp()
        self.data = {
            "title": "title",
            "filename": "filename",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201_if_user_is_staff(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_post(
            views.GlobalTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_403_if_user_is_superuser(self):
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_post(
            views.GlobalTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_403_if_user_does_not_have_permission(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_post(
            views.GlobalTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_owner_is_global(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)
        mock_request = create_mock_request(user=user)

        # Act
        response = RequestMock.do_request_post(
            views.GlobalTemplateList.as_view(), user, data=self.data
        )

        # get template version manager from posted template
        template_id = response.data["id"]
        template_object = template_api.get(template_id, request=mock_request)
        template_version_manager = vm_api.get_from_version(
            template_object, request=mock_request
        )

        # Assert
        self.assertEqual(template_version_manager.user, None)


class TestCurrentTemplateVersion(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def test_patch_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_disabled_returns_http_400(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_2_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDisableTemplateVersion(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def test_patch_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_already_disabled_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_current_returns_http_400(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_3.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_2_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRestoreTemplateVersion(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def test_patch_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_disabled_returns_http_400(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_1_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": str(self.fixture.template_2_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDisableTemplateVersionManager(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def test_patch_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_already_disabled_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.fixture.template_vm_1.is_disabled = True

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestRestoreTemplateVersionManager(MongoIntegrationBaseTestCase):
    fixture = fixture_template

    def test_patch_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)
        self.fixture.template_vm_1.is_disabled = True

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": "507f1f77bcf86cd799439011"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_disabled_returns_http_200(self):
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_global_as_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_other_user_returns_http_403(self):
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": str(self.fixture.template_vm_2.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
