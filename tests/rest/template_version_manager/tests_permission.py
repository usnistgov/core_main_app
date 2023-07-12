""" Authentication tests for Template Version Manager REST API
"""
from unittest.mock import patch

from core_main_app.access_control.exceptions import AccessControlError
from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.rest.template_version_manager import (
    views as template_version_manager_views,
)
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.rest.template_version_manager.serializers import (
    TemplateVersionManagerSerializer,
    CreateTemplateSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGlobalTemplateVersionManagerListGetPermission(SimpleTestCase):
    """TestGlobalTemplateVersionManagerListGetPermission"""

    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_anonymous_returns_http_403(
        self, template_version_manager_get_all_global_version_managers
    ):
        """test_anonymous_returns_http_403

        Args:
            template_version_manager_get_all_global_version_managers:

        Returns:

        """
        template_version_manager_get_all_global_version_managers.return_value = TemplateVersionManager(
            user=None
        )

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_global_version_managers")
    def test_authenticated_returns_http_200(
        self, template_version_manager_get_all_global_version_managers
    ):
        """test_authenticated_returns_http_200

        Args:
            template_version_manager_get_all_global_version_managers:

        Returns:

        """
        template_version_manager_get_all_global_version_managers.return_value = (
            {}
        )

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
        """test_staff_returns_http_200

        Args:
            template_version_manager_get_all_global_version_managers:

        Returns:

        """
        template_version_manager_get_all_global_version_managers.return_value = (
            {}
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserTemplateVersionManagerListGetPermission(SimpleTestCase):
    """TestUserTemplateVersionManagerListGetPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_all_version_manager_by_user_id")
    def test_authenticated_returns_http_200(
        self, template_version_manager_get_all_version_manager_by_user_id
    ):
        """test_authenticated_returns_http_200

        Args:
            template_version_manager_get_all_version_manager_by_user_id:

        Returns:

        """
        template_version_manager_get_all_version_manager_by_user_id.return_value = (
            {}
        )

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
        """test_staff_returns_http_200

        Args:
            template_version_manager_get_all_version_manager_by_user_id:

        Returns:

        """
        template_version_manager_get_all_version_manager_by_user_id.return_value = (
            {}
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionManagerDetailGetPermission(SimpleTestCase):
    """TestTemplateVersionManagerDetailGetPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_by_id")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_authenticated_returns_http_200(
        self, template_version_manager_data, version_manager_get_by_id
    ):
        """test_authenticated_returns_http_200

        Args:
            template_version_manager_data:
            version_manager_get_by_id:

        Returns:

        """
        template_version_manager_data.return_value = True
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_by_id")
    @patch.object(TemplateVersionManagerSerializer, "data")
    def test_staff_returns_http_200(
        self, template_version_manager_data, version_manager_get_by_id
    ):
        """test_staff_returns_http_200

        Args:
            template_version_manager_data:
            version_manager_get_by_id:

        Returns:

        """
        template_version_manager_data.return_value = True
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.TemplateVersionManagerDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionPostPermission(SimpleTestCase):
    """TestTemplateVersionPostPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            template_version_manager_views.TemplateVersion.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            template_version_manager_views.TemplateVersion.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_by_id")
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
        """test_staff_returns_http_201

        Args:
            template_version_manager_serializer_data:
            template_version_manager_serializer_save:
            template_version_manager_serializer_valid:
            version_manager_get_by_id:

        Returns:

        """
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user=None
        )
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
    """TestUserTemplateListPostPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
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
        """test_authenticated_returns_http_201

        Args:
            template_version_manager_serializer_data:
            template_version_manager_serializer_save:
            template_version_manager_serializer_valid:
            create_template_version_manager_serializer_data:
            create_template_version_manager_serializer_save:
            create_template_version_manager_serializer_valid:

        Returns:

        """
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
        """test_staff_returns_http_201

        Args:
            template_version_manager_serializer_data:
            template_version_manager_serializer_save:
            template_version_manager_serializer_valid:
            create_template_version_manager_serializer_data:
            create_template_version_manager_serializer_save:
            create_template_version_manager_serializer_valid:

        Returns:

        """
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
    """TestGlobalTemplateListPostPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            template_version_manager_views.GlobalTemplateList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
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
        """test_staff_returns_http_201

        Args:
            template_version_manager_serializer_data:
            template_version_manager_serializer_save:
            template_version_manager_serializer_valid:
            create_template_version_manager_serializer_data:
            create_template_version_manager_serializer_save:
            create_template_version_manager_serializer_valid:

        Returns:

        """
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
    """TestCurrentTemplateVersionPatchPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.set_current")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_set_current,
    ):
        """test_staff_returns_http_200

        Args:
            template_get_by_id:
            version_manager_set_current:

        Returns:

        """
        version_manager_set_current.return_value = {}
        # version_manager_get_from_version.return_value = VersionManager(user="1")
        template_get_by_id.return_value = Template(user="1")

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.CurrentTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDisableTemplateVersionPatchPermission(SimpleTestCase):
    """TestDisableTemplateVersionPatchPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.disable_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_disable_version,
    ):
        """test_staff_returns_http_200

        Args:
            template_get_by_id:
            version_manager_disable_version:

        Returns:

        """
        version_manager_disable_version.return_value = TemplateVersionManager(
            user="1"
        )
        template_get_by_id.return_value = Template(user="1")

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRestoreTemplateVersionPatchPermission(SimpleTestCase):
    """TestRestoreTemplateVersionPatchPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Returns:

        """
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.restore_version")
    @patch.object(Template, "get_by_id")
    def test_staff_returns_http_200(
        self,
        template_get_by_id,
        version_manager_restore_version,
    ):
        """test_staff_returns_http_200

        Args:
            template_get_by_id:
            version_manager_restore_version:

        Returns:

        """
        version_manager_restore_version.return_value = {}
        template_get_by_id.return_value = Template(user="1")

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersion.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDisableTemplateVersionManagerPatchPermission(SimpleTestCase):
    """TestDisableTemplateVersionManagerPatchPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(TemplateVersionManager, "get_by_id")
    @patch("core_main_app.components.version_manager.api.disable")
    def test_authenticated_returns_http_200(
        self, version_manager_disable, version_manager_get_by_id
    ):
        """test_authenticated_returns_http_200

        Args:
            version_manager_disable:
            version_manager_get_by_id:

        Returns:

        """
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )
        version_manager_disable.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(TemplateVersionManager, "get_by_id")
    @patch("core_main_app.components.version_manager.api.disable")
    def test_staff_returns_http_200(
        self, version_manager_disable, version_manager_get_by_id
    ):
        """test_staff_returns_http_200

        Args:
            version_manager_disable:
            version_manager_get_by_id:

        Returns:

        """
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )
        version_manager_disable.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.DisableTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRestoreTemplateVersionManagerPatchPermission(SimpleTestCase):
    """TestRestoreTemplateVersionManagerPatchPermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            None,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.version_manager.api.restore")
    @patch.object(TemplateVersionManager, "get_by_id")
    def test_authenticated_returns_http_200(
        self, version_manager_get_by_id, version_manager_restore
    ):
        """test_authenticated_returns_http_200

        Args:
            version_manager_get_by_id:
            version_manager_restore:

        Returns:

        """
        version_manager_restore.return_value = {}
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.version_manager.api.restore")
    @patch.object(TemplateVersionManager, "get_by_id")
    def test_staff_returns_http_200(
        self, version_manager_get_by_id, version_manager_restore
    ):
        """test_staff_returns_http_200

        Args:
            version_manager_get_by_id:
            version_manager_restore:

        Returns:

        """
        version_manager_restore.return_value = {}
        version_manager_get_by_id.return_value = TemplateVersionManager(
            user="1"
        )

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            template_version_manager_views.RestoreTemplateVersionManager.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestTemplateVersionManagerListGetPermission(SimpleTestCase):
    """TestGlobalTemplateVersionManagerListGetPermission"""

    @patch.object(template_version_manager_api, "get_all")
    def test_anonymous_returns_http_403(
        self, template_version_manager_get_all
    ):
        """test_anonymous_returns_http_403

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = TemplateVersionManager(
            user=None
        )

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalAndUserTemplateVersionManagerList.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_version_manager_api, "get_all")
    def test_authenticated_returns_http_403(
        self, template_version_manager_get_all
    ):
        """test_authenticated_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalAndUserTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_version_manager_api, "get_all")
    def test_staff_returns_http_200(self, template_version_manager_get_all):
        """test_staff_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalAndUserTemplateVersionManagerList.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGlobalTemplateVersionManagerOrderingListGetPermission(
    SimpleTestCase
):
    """Test Template Version Manager Ordering List Get Permission"""

    def test_anonymous_returns_http_403(
        self,
    ):
        """test_anonymous_returns_http_403

        Args:

        Returns:

        """
        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            None,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403

        Args:

        Returns:

        """

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_version_manager_api, "get_global_version_managers")
    def test_staff_returns_http_200(self, template_version_manager_get_all):
        """test_staff_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_version_manager_api, "get_global_version_managers")
    def test_superuser_returns_http_200(
        self, template_version_manager_get_all
    ):
        """test_superuser_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGlobalTemplateVersionManagerOrderingPatchPermission(SimpleTestCase):
    """Test Template Version Manager Ordering Patch Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            None,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.template_version_manager.api.get_global_version_managers"
    )
    def test_authenticated_returns_http_403(
        self, mock_get_global_version_managers
    ):
        """test_staff_returns_http_403

        Args:


        Returns:

        """
        mock_get_global_version_managers.side_effect = AccessControlError("")
        response = RequestMock.do_request_patch(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            create_mock_user("1"),
            data={"template_list": []},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.template_version_manager.api.get_global_version_managers"
    )
    @patch(
        "core_main_app.components.template_version_manager.api.update_global_template_ordering"
    )
    def test_staff_returns_http_200(
        self,
        mock_get_global_version_managers,
        mock_update_templates_ordering,
    ):
        """test_staff_returns_http_200

        Args:
            mock_get_global_version_managers:
            mock_update_templates_ordering:

        Returns:

        """
        mock_user = create_mock_user("1", is_staff=True)
        mock_get_global_version_managers.return_value = []
        mock_update_templates_ordering.return_value = []
        response = RequestMock.do_request_patch(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            mock_user,
            data={"template_list": []},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.template_version_manager.api.get_global_version_managers"
    )
    @patch(
        "core_main_app.components.template_version_manager.api.update_global_template_ordering"
    )
    def test_superuser_returns_http_200(
        self,
        mock_get_global_version_managers,
        mock_update_templates_ordering,
    ):
        """test_superuser_returns_http_200

        Args:
            mock_get_global_version_managers:
            mock_update_templates_ordering:

        Returns:

        """
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
        mock_get_global_version_managers.return_value = []
        mock_update_templates_ordering.return_value = []
        response = RequestMock.do_request_patch(
            template_version_manager_views.GlobalTemplateVersionManagerOrdering.as_view(),
            mock_user,
            data={"template_list": []},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserTemplateVersionManagerOrderingListGetPermission(SimpleTestCase):
    """Test Template Version Manager Ordering List Get Permission"""

    def test_anonymous_returns_http_403(
        self,
    ):
        """test_anonymous_returns_http_403

        Args:

        Returns:

        """
        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            None,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(template_version_manager_api, "get_all_by_user_id")
    def test_authenticated_returns_http_200(
        self, template_version_manager_get_all_by_user_id
    ):
        """test_authenticated_returns_http_200

        Args:
            template_version_manager_get_all_by_user_id:

        Returns:

        """
        template_version_manager_get_all_by_user_id.return_value = {}

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_version_manager_api, "get_all_by_user_id")
    def test_staff_returns_http_200(self, template_version_manager_get_all):
        """test_staff_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(template_version_manager_api, "get_all_by_user_id")
    def test_superuser_returns_http_200(
        self, template_version_manager_get_all
    ):
        """test_superuser_returns_http_200

        Args:
            template_version_manager_get_all:

        Returns:

        """
        template_version_manager_get_all.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserTemplateVersionManagerOrderingPatchPermission(SimpleTestCase):
    """Test Template Version Manager Ordering Patch Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            None,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(
        "core_main_app.components.template_version_manager.api.get_all_by_user_id"
    )
    @patch(
        "core_main_app.components.template_version_manager.api.update_user_template_ordering"
    )
    def test_authenticated_returns_http_200(
        self,
        mock_get_all_by_user_id,
        mock_update_templates_ordering,
    ):
        """test_staff_returns_http_200

        Args:
            mock_get_all_by_user_id:
            mock_update_templates_ordering:

        Returns:

        """
        mock_user = create_mock_user("1")
        mock_get_all_by_user_id.return_value = []
        mock_update_templates_ordering.return_value = []
        response = RequestMock.do_request_patch(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
            data={"template_list": []},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.template_version_manager.api.get_by_id_list"
    )
    @patch(
        "core_main_app.components.template_version_manager.api.update_user_template_ordering"
    )
    @patch.object(template_version_manager_api, "get_all_by_user_id")
    def test_staff_returns_http_200(
        self,
        mock_get_by_user_id,
        mock_update_templates_ordering,
        mock_get_all_by_user_id,
    ):
        """test_staff_returns_http_200

        Args:
            mock_get_all_by_user_id:
            mock_update_templates_ordering:

        Returns:

        """
        mock_user = create_mock_user("1", is_staff=True)
        mock_get_all_by_user_id.return_value = []
        mock_get_by_user_id.return_value = []
        mock_update_templates_ordering.return_value = []
        response = RequestMock.do_request_patch(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
            data={"template_list": []},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.template_version_manager.api.get_by_id_list"
    )
    @patch(
        "core_main_app.components.template_version_manager.api.update_user_template_ordering"
    )
    @patch.object(template_version_manager_api, "get_all_by_user_id")
    def test_superuser_returns_http_200(
        self,
        mock_get_by_user_id,
        mock_update_templates_ordering,
        mock_get_all_by_user_id,
    ):
        """test_superuser_returns_http_200

        Args:
            mock_get_all_by_user_id:
            mock_update_templates_ordering:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_get_all_by_user_id.return_value = []
        mock_get_by_user_id.return_value = []
        mock_update_templates_ordering.return_value = []
        response = RequestMock.do_request_patch(
            template_version_manager_views.UserTemplateVersionManagerOrdering.as_view(),
            mock_user,
            data={"template_list": []},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
