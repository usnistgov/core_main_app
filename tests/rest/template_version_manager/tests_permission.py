""" Authentication tests for Template Version Manager REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.version_manager.models import VersionManager
from core_main_app.rest.template_version_manager import (
    views as template_version_manager_views,
)
from core_main_app.rest.template_version_manager.serializers import (
    TemplateVersionManagerSerializer,
    CreateTemplateSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGlobalTemplateVersionManagerListGetPermission(SimpleTestCase):
    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_anonymous_returns_http_200(
        self, template_version_manager_get_all_global_version_managers
    ):
        template_version_manager_get_all_global_version_managers.return_value = {}

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_authenticated_returns_http_200(
        self, template_version_manager_get_all_global_version_managers
    ):
        template_version_manager_get_all_global_version_managers.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_staff_returns_http_200(
        self, template_version_manager_get_all_global_version_managers
    ):
        template_version_manager_get_all_global_version_managers.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserTemplateVersionManagerListGetPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_all_version_manager_by_user_id")
    def test_authenticated_returns_http_200(
        self, template_version_manager_get_all_version_manager_by_user_id
    ):
        template_version_manager_get_all_version_manager_by_user_id.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_all_version_manager_by_user_id")
    def test_staff_returns_http_200(
        self, template_version_manager_get_all_version_manager_by_user_id
    ):
        template_version_manager_get_all_version_manager_by_user_id.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionManagerDetailGetPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(VersionManager, "get_by_id")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_authenticated_returns_http_200(
        self, template_version_manager_data, version_manager_get_by_id
    ):
        template_version_manager_data.return_value = True
        version_manager_get_by_id.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(VersionManager, "get_by_id")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_staff_returns_http_200(
        self, template_version_manager_data, version_manager_get_by_id
    ):
        template_version_manager_data.return_value = True
        version_manager_get_by_id.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionPostPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            template_version_manager_views.TemplateVersion.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_version_manager_views.TemplateVersion.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(VersionManager, "get_by_id")
    @patch.object(CreateTemplateSerializer, "is_valid")
    @patch.object(CreateTemplateSerializer, "save")
    @patch.object(CreateTemplateSerializer, "data")
    def test_staff_returns_http_201(
        self,
        template_version_manager_serializer_data,
        template_version_manager_serializer_save,
        template_version_manager_serializer_valid,
        version_manager_get_by_id,
    ):
        version_manager_get_by_id.return_value = {}
        template_version_manager_serializer_data.return_value = True
        template_version_manager_serializer_save.return_value = None
        template_version_manager_serializer_valid.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            template_version_manager_views.TemplateVersion.as_view(),
            mock_user,
            data={},
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestUserTemplateListPostPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            template_version_manager_views.UserTemplateList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CreateTemplateSerializer, "is_valid")
    @patch.object(CreateTemplateSerializer, "save")
    @patch.object(CreateTemplateSerializer, "data")
    @patch.object(TemplateVersionManagerSerializer, "is_valid")
    @patch.object(TemplateVersionManagerSerializer, "save")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_authenticated_returns_http_201(
        self,
        template_version_manager_serializer_data,
        template_version_manager_serializer_save,
        template_version_manager_serializer_valid,
        create_template_version_manager_serializer_data,
        create_template_version_manager_serializer_save,
        create_template_version_manager_serializer_valid,
    ):
        create_template_version_manager_serializer_data.return_value = True
        create_template_version_manager_serializer_save.return_value = None
        create_template_version_manager_serializer_valid.return_value = {}
        template_version_manager_serializer_data.return_value = True
        template_version_manager_serializer_save.return_value = None
        template_version_manager_serializer_valid.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_version_manager_views.UserTemplateList.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch.object(CreateTemplateSerializer, "is_valid")
    @patch.object(CreateTemplateSerializer, "save")
    @patch.object(CreateTemplateSerializer, "data")
    @patch.object(TemplateVersionManagerSerializer, "is_valid")
    @patch.object(TemplateVersionManagerSerializer, "save")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_staff_returns_http_201(
        self,
        template_version_manager_serializer_data,
        template_version_manager_serializer_save,
        template_version_manager_serializer_valid,
        create_template_version_manager_serializer_data,
        create_template_version_manager_serializer_save,
        create_template_version_manager_serializer_valid,
    ):
        create_template_version_manager_serializer_data.return_value = True
        create_template_version_manager_serializer_save.return_value = None
        create_template_version_manager_serializer_valid.return_value = {}
        template_version_manager_serializer_data.return_value = True
        template_version_manager_serializer_save.return_value = None
        template_version_manager_serializer_valid.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            template_version_manager_views.UserTemplateList.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestGlobalTemplateListPostPermission(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            template_version_manager_views.GlobalTemplateList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_version_manager_views.GlobalTemplateList.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CreateTemplateSerializer, "is_valid")
    @patch.object(CreateTemplateSerializer, "save")
    @patch.object(CreateTemplateSerializer, "data")
    @patch.object(TemplateVersionManagerSerializer, "is_valid")
    @patch.object(TemplateVersionManagerSerializer, "save")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_staff_returns_http_201(
        self,
        template_version_manager_serializer_data,
        template_version_manager_serializer_save,
        template_version_manager_serializer_valid,
        create_template_version_manager_serializer_data,
        create_template_version_manager_serializer_save,
        create_template_version_manager_serializer_valid,
    ):
        create_template_version_manager_serializer_data.return_value = True
        create_template_version_manager_serializer_save.return_value = None
        create_template_version_manager_serializer_valid.return_value = {}
        template_version_manager_serializer_data.return_value = True
        template_version_manager_serializer_save.return_value = None
        template_version_manager_serializer_valid.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            template_version_manager_views.GlobalTemplateList.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestCurrentTemplateVersionPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.set_current")
    @patch("core_main_app.components.version_manager.api.get_from_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_get_from_version,
        version_manager_set_current,
    ):
        version_manager_set_current.return_value = {}
        version_manager_get_from_version.return_value = {}
        template_get_by_id.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDisableTemplateVersionPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.disable_version")
    @patch("core_main_app.components.version_manager.api.get_from_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_get_from_version,
        version_manager_disable_version,
    ):
        version_manager_disable_version.return_value = {}
        version_manager_get_from_version.return_value = {}
        template_get_by_id.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRestoreTemplateVersionPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.restore_version")
    @patch("core_main_app.components.version_manager.api.get_from_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_get_from_version,
        version_manager_restore_version,
    ):
        version_manager_restore_version.return_value = {}
        version_manager_get_from_version.return_value = {}
        template_get_by_id.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDisableTemplateVersionManagerPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(VersionManager, "get_by_id")
    @patch("core_main_app.components.version_manager.api.disable")
    def test_authenticated_returns_http_200(
        self, version_manager_disable, version_manager_get_by_id
    ):
        version_manager_get_by_id.return_value = TemplateVersionManager(user="1")
        version_manager_disable.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(VersionManager, "get_by_id")
    @patch("core_main_app.components.version_manager.api.disable")
    def test_staff_returns_http_200(
        self, version_manager_disable, version_manager_get_by_id
    ):
        version_manager_get_by_id.return_value = TemplateVersionManager(user="2")
        version_manager_disable.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRestoreTemplateVersionManagerPatchPermission(SimpleTestCase):
    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.restore")
    @patch.object(VersionManager, "get_by_id")
    def test_authenticated_returns_http_200(
        self, version_manager_get_by_id, version_manager_restore
    ):
        version_manager_restore.return_value = {}
        version_manager_get_by_id.return_value = TemplateVersionManager(user="1")
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.version_manager.api.restore")
    @patch.object(VersionManager, "get_by_id")
    def test_staff_returns_http_200(
        self, version_manager_get_by_id, version_manager_restore
    ):
        version_manager_restore.return_value = {}
        version_manager_get_by_id.return_value = TemplateVersionManager(user="2")

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
