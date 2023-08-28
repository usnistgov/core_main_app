""" Integration Test for Template Version Manager Rest API
"""
import json

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from tests.components.template_version_manager.fixtures.fixtures import (
    TemplateVersionManagerFixtures,
    TemplateVersionManagerOrderingFixtures,
    TemplateVersionManagerAccessControlFixtures,
)

from core_main_app.components.template import api as template_api
from core_main_app.rest.template_version_manager import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import (
    RequestMock,
    create_mock_request,
)

fixture_template = TemplateVersionManagerFixtures()
fixture_template_2 = TemplateVersionManagerAccessControlFixtures()
fixture_template_vm_ordering = TemplateVersionManagerOrderingFixtures()


class TestGlobalTemplateVersionManagerList(IntegrationBaseTestCase):
    """TestGlobalTemplateVersionManagerList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_global_tvm(self):
        """test_get_returns_all_global_tvm

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_returned_tvm_are_global(self):
        """test_get_returned_tvm_are_global

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.data[0]["user"], None)

    def test_get_filtered_by_correct_title_returns_tvm(self):
        """test_get_filtered_by_correct_title_returns_tvm

        Returns:

        """
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
        """test_get_filtered_by_incorrect_title_returns_no_tvm

        Returns:

        """
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
        """test_get_filtered_by_expected_is_disabled_returns_tvm

        Returns:

        """
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
        """test_get_filtered_by_incorrect_is_disabled_returns_no_tvm

        Returns:

        """
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


class TestUserTemplateVersionManagerList(IntegrationBaseTestCase):
    """TestUserTemplateVersionManagerList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_user_tvm(self):
        """test_get_returns_all_user_tvm

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_returned_tvm_are_from_user(self):
        """test_get_returned_tvm_are_from_user

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerList.as_view(), user
        )

        # Assert
        self.assertEqual(response.data[0]["user"], "1")

    def test_get_filtered_by_correct_title_returns_tvm(self):
        """test_get_filtered_by_correct_title_returns_tvm

        Returns:

        """
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
        """test_get_filtered_by_incorrect_title_returns_no_tvm

        Returns:

        """
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
        """test_get_filtered_by_expected_is_disabled_returns_tvm

        Returns:

        """
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
        """test_get_filtered_by_incorrect_is_disabled_returns_no_tvm

        Returns:

        """
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


class TestTemplateVersionManagerDetail(IntegrationBaseTestCase):
    """TestTemplateVersionManagerDetail"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
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
        """test_get_returns_tvm

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            user,
            param={"pk": self.fixture.template_vm_1.id},
        )

        # Assert
        self.assertEqual(
            response.data["title"], self.fixture.template_vm_1.title
        )

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            views.TemplateVersionManagerDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTemplateVersion(IntegrationBaseTestCase):
    """TestTemplateVersion"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {
            "filename": "filename",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    def post_returns_http_201(self):
        """post_returns_http_201

        Returns:

        """
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
        """post_wrong_id_returns_http_404

        Returns:

        """
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
        """post_to_other_user_returns_http_403

        Returns:

        """
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
        """post_to_other_user_as_superuser_returns_http_201

        Returns:

        """
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
        """post_to_global_as_superuser_returns_http_201

        Returns:

        """
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
        """post_to_global_as_user_returns_http_403

        Returns:

        """
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


class TestUserTemplateList(IntegrationBaseTestCase):
    """TestUserTemplateList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {
            "title": "title",
            "filename": "filename.xsd",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201(self):
        """test_post_returns_http_201

        Returns:

        """
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
        """test_post_owner_is_user

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        mock_request = create_mock_request(user=user)

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # get template version manager from posted template
        template_id = response.data["id"]
        template_object = template_api.get_by_id(
            template_id, request=mock_request
        )

        # Assert
        self.assertEqual(template_object.version_manager.user, user.id)

    def test_post_template_name_already_exists_returns_http_400(self):
        """test_post_template_name_already_exists_returns_http_400

        Returns:

        """
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
        """test_post_template_with_correct_dependency_returns_http_201

        Returns:

        """
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
    def test_post_template_with_incorrect_dependency_schema_location_returns_http_400(
        self,
    ):
        """test_post_template_with_incorrect_dependency_schema_location_returns_http_400

        Returns:

        """
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
        """test_post_template_with_incorrect_dependency_id_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        self.data["content"] = (
            "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:include schemaLocation='template1_1.xsd'/>"
            "<xs:element name='root'/></xs:schema>"
        )

        self.data["dependencies_dict"] = json.dumps(
            {"template1_1.xsd": "bad_id"}
        )

        # Act
        response = RequestMock.do_request_post(
            views.UserTemplateList.as_view(), user, data=self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGlobalTemplateList(IntegrationBaseTestCase):
    """TestGlobalTemplateList"""

    fixture = fixture_template

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {
            "title": "title",
            "filename": "filename.xsd",
            "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
            "<xs:element name='root'/></xs:schema>",
        }

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201_if_user_is_staff(self):
        """test_post_returns_http_201_if_user_is_staff

        Returns:

        """
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
        """test_post_returns_http_403_if_user_is_superuser

        Returns:

        """
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
        """test_post_returns_http_403_if_user_does_not_have_permission

        Returns:

        """
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
        """test_post_owner_is_global

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)
        mock_request = create_mock_request(user=user)

        # Act
        response = RequestMock.do_request_post(
            views.GlobalTemplateList.as_view(), user, data=self.data
        )

        # get template version manager from posted template
        template_id = response.data["id"]
        template_object = template_api.get_by_id(
            template_id, request=mock_request
        )

        # Assert
        self.assertEqual(template_object.version_manager.user, None)


class TestCurrentTemplateVersion(IntegrationBaseTestCase):
    """TestCurrentTemplateVersion"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200

        Returns:

        """
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
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.CurrentTemplateVersion.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_disabled_returns_http_400(self):
        """test_patch_disabled_returns_http_400

        Returns:

        """
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
        """test_patch_global_as_user_returns_http_403

        Returns:

        """
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
        """test_patch_other_user_returns_http_403

        Returns:

        """
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


class TestDisableTemplateVersion(IntegrationBaseTestCase):
    """TestDisableTemplateVersion"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200

        Returns:

        """
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
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersion.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_already_disabled_returns_http_200(self):
        """test_patch_already_disabled_returns_http_200

        Returns:

        """
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
        """test_patch_current_returns_http_400

        Returns:

        """
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
        """test_patch_global_as_user_returns_http_403

        Returns:

        """
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
        """test_patch_other_user_returns_http_403

        Returns:

        """
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


class TestRestoreTemplateVersion(IntegrationBaseTestCase):
    """TestRestoreTemplateVersion"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200

        Returns:

        """
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
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersion.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_disabled_returns_http_400(self):
        """test_patch_not_disabled_returns_http_400

        Returns:

        """
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
        """test_patch_global_as_user_returns_http_403

        Returns:

        """
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
        """test_patch_other_user_returns_http_403

        Returns:

        """
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


class TestDisableTemplateVersionManager(IntegrationBaseTestCase):
    """TestDisableTemplateVersionManager"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200

        Returns:

        """
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
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.DisableTemplateVersionManager.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_already_disabled_returns_http_200(self):
        """test_patch_already_disabled_returns_http_200

        Returns:

        """
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
        """test_patch_global_as_user_returns_http_403

        Returns:

        """
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
        """test_patch_other_user_returns_http_403

        Returns:

        """
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


class TestRestoreTemplateVersionManager(IntegrationBaseTestCase):
    """TestRestoreTemplateVersionManager"""

    fixture = fixture_template

    def test_patch_returns_http_200(self):
        """test_patch_returns_http_200

        Returns:

        """
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
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            views.RestoreTemplateVersionManager.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_not_disabled_returns_http_200(self):
        """test_patch_not_disabled_returns_http_200

        Returns:

        """
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
        """test_patch_global_as_user_returns_http_403

        Returns:

        """
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
        """test_patch_other_user_returns_http_403

        Returns:

        """
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


class UserTemplateVersionManagerOrdering(IntegrationBaseTestCase):
    """User Template Version Manager Ordering"""

    fixture = fixture_template_vm_ordering

    def test_get_as_owner_returns_all_user_template_version_managers(self):
        """test_get_as_owner_returns_all_user_template_version_managers

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_as_owner_returns_empty_list(self):
        """test_get_as_owner_returns_empty_list

        Returns:

        """
        # Arrange
        user = create_mock_user("2")
        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_as_superuser_returns_all_user_template_version_managers(self):
        """test_get_as_superuser_returns_all_user_template_version_managers

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)
        # Act
        response = RequestMock.do_request_get(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_patch_as_owner_updates_template_version_manager_ordering(self):
        """test_patch_as_owner_updates_template_version_manager_ordering

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [self.fixture.tvm2.id, self.fixture.tvm1.id]
            },
        )
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["display_rank"], 1)
        self.assertEqual(response.data[0]["id"], self.fixture.tvm2.id)
        self.assertEqual(response.data[1]["display_rank"], 2)
        self.assertEqual(response.data[1]["id"], self.fixture.tvm1.id)

    def test_patch_wrong_ids_returns_http_404(self):
        """test_patch_wrong_ids_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.tvm2.id,
                    -1,
                    self.fixture.tvm1.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_inaccessible_id_returns_http_403(self):
        """test_patch_wrong_ids_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.tvm2.id,
                    self.fixture.global_tvm2.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_duplicate_ids_returns_http_400(self):
        """test_patch_duplicate_ids_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [self.fixture.tvm2.id, self.fixture.tvm2.id]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_others_template_version_manager_returns_http_403(self):
        """test_patch_returns_updates_template_version_manager_order

        Returns:

        """
        # Arrange
        user = create_mock_user("2")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [self.fixture.tvm2.id, self.fixture.tvm1.id]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_without_param__returns_http_500(self):
        """test_patch_returns_updates_template_version_manager_order

        Returns:

        """
        # Arrange
        user = create_mock_user("2")
        # Act
        response = RequestMock.do_request_patch(
            views.UserTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class GlobalTemplateVersionManagerOrdering(IntegrationBaseTestCase):
    """Global Template Version Manager Ordering"""

    fixture = fixture_template_vm_ordering

    def test_get_as_user_returns_http_403(self):
        """test_get_as_user_returns_all_global_template_version_managers

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_as_superuser_returns_all_global_template_version_managers(
        self,
    ):
        """test_get_as_superuser_returns_all_global_template_version_managers

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)
        # Act
        response = RequestMock.do_request_get(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_patch_as_user_returns_error_403(self):
        """test_patch_as_user_returns_error_403

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        # Act
        response = RequestMock.do_request_patch(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.global_tvm2.id,
                    self.fixture.global_tvm1.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_as_superuser_updates_template_version_manager_ordering(
        self,
    ):
        """test_patch_as_superuser_updates_template_version_manager_ordering

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)
        # Act
        response = RequestMock.do_request_patch(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.global_tvm2.id,
                    self.fixture.global_tvm1.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["display_rank"], 1)
        self.assertEqual(response.data[0]["id"], self.fixture.global_tvm2.id)
        self.assertEqual(response.data[1]["display_rank"], 2)
        self.assertEqual(response.data[1]["id"], self.fixture.global_tvm1.id)

    def test_patch_wrong_ids_returns_http_404(self):
        """test_patch_wrong_ids_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)
        # Act
        response = RequestMock.do_request_patch(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.global_tvm2.id,
                    -1,
                    self.fixture.global_tvm1.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_duplicate_ids_returns_http_400(self):
        """test_patch_duplicate_ids_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user("1", is_staff=True, is_superuser=True)
        # Act
        response = RequestMock.do_request_patch(
            views.GlobalTemplateVersionManagerOrdering.as_view(),
            user,
            data={
                "template_list": [
                    self.fixture.global_tvm2.id,
                    self.fixture.global_tvm2.id,
                ]
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestTemplateVersionManagerList(IntegrationBaseTestCase):
    """TestTemplateVersionManagerList"""

    fixture = fixture_template_2

    def setUp(self):
        """setUp

        Returns:

        """
        self.user = create_mock_user("1", is_superuser=True, is_staff=True)
        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """

        # Act
        response = RequestMock.do_request_get(
            views.GlobalAndUserTemplateVersionManagerList.as_view(), self.user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_tvm(self):
        """test_get_returns_all_tvm_when_is_user_template_selected_is_true

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            views.GlobalAndUserTemplateVersionManagerList.as_view(),
            self.user,
        )

        # Assert
        self.assertEqual(len(response.data), 3)
