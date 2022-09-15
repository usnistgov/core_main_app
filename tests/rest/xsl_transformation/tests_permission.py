""" Authentication tests for Template REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_main_app.components.xsl_transformation.models import XslTransformation
from core_main_app.rest.xsl_transformation import views as xslt_views
from core_main_app.rest.xsl_transformation.serializers import (
    XslTransformationSerializer,
    TransformSerializer,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestXslTransformationListGetPermission(SimpleTestCase):
    """TestXslTransformationListGetPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_anonymous=True),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "get_all")
    @patch.object(XslTransformationSerializer, "data")
    def test_is_staff_returns_http_200(self, xslt_serializer_data, xslt_get_all):
        """test_is_staff_returns_http_200

        Args:
            xslt_serializer_data:
            xslt_get_all:

        Returns:

        """
        xslt_get_all.return_value = {}
        xslt_serializer_data.return_value = True

        response = RequestMock.do_request_get(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_staff=True),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestXslTransformationListPostPermission(SimpleTestCase):
    """TestXslTransformationListPostPermission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_anonymous=True),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "get_all")
    @patch.object(XslTransformationSerializer, "is_valid")
    @patch.object(XslTransformationSerializer, "save")
    @patch.object(XslTransformationSerializer, "data")
    def test_is_staff_returns_http_201(
        self,
        xslt_serializer_data,
        xslt_serializer_save,
        xslt_serializer_is_valid,
        xslt_get_all,
    ):
        """test_is_staff_returns_http_201

        Args:
            xslt_serializer_data:
            xslt_serializer_save:
            xslt_serializer_is_valid:
            xslt_get_all:

        Returns:

        """
        xslt_get_all.return_value = {}
        xslt_serializer_is_valid.return_value = {}
        xslt_serializer_save.return_value = None
        xslt_serializer_data.return_value = True

        response = RequestMock.do_request_post(
            xslt_views.XslTransformationList.as_view(),
            create_mock_user("1", is_staff=True),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestXslTransformationDetailGetPermission(SimpleTestCase):
    """TestXslTransformationDetailGetPermission"""

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
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_get(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "get_by_id")
    @patch.object(XslTransformationSerializer, "data")
    def test_is_staff_returns_http_200(self, xslt_serializer_data, xslt_get_by_id):
        """test_is_staff_returns_http_200

        Args:
            xslt_serializer_data:
            xslt_get_by_id:

        Returns:

        """
        xslt_get_by_id.return_value = {}
        xslt_serializer_data.return_value = True

        response = RequestMock.do_request_get(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_staff=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestXslTransformationDetailDeletePermission(SimpleTestCase):
    """TestXslTransformationDetailDeletePermission"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(
        self,
    ):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_delete(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_delete(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "delete")
    @patch.object(XslTransformation, "get_by_id")
    @patch.object(XslTransformationSerializer, "data")
    def test_is_staff_returns_http_204(
        self, xslt_serializer_data, xslt_get_by_id, xslt_delete
    ):
        """test_is_staff_returns_http_204

        Args:
            xslt_serializer_data:
            xslt_get_by_id:
            xslt_delete:

        Returns:

        """
        xslt_get_by_id.return_value = XslTransformation(
            name="mock", filename="mock", content="mock"
        )
        xslt_serializer_data.return_value = True

        response = RequestMock.do_request_delete(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_staff=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestXslTransformationDetailPatchPermission(SimpleTestCase):
    """TestXslTransformationDetailPatchPermission"""

    def setUp(self):
        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(
        self,
    ):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=True),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_authenticated_returns_http_403(self):
        """test_is_authenticated_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_patch(
            xslt_views.XslTransformationDetail.as_view(),
            create_mock_user("1", is_anonymous=False),
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "get_by_id")
    @patch.object(XslTransformationSerializer, "is_valid")
    @patch.object(XslTransformationSerializer, "save")
    @patch.object(XslTransformationSerializer, "data")
    def test_is_staff_returns_http_200(
        self,
        xslt_serializer_data,
        xslt_serializer_save,
        xslt_serializer_is_valid,
        xslt_get_by_id,
    ):
        """test_is_staff_returns_http_200

        Args:
            xslt_serializer_data:
            xslt_serializer_save:
            xslt_serializer_is_valid:
            xslt_get_by_id:

        Returns:

        """
        xslt_get_by_id.return_value = {}
        xslt_serializer_is_valid.return_value = {}
        xslt_serializer_save.return_value = None
        xslt_serializer_data.return_value = True

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            xslt_views.XslTransformationDetail.as_view(),
            mock_user,
            param={"pk": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestXslTransformationTransformPostPermission(SimpleTestCase):
    """test_is_staff_returns_http_200"""

    def test_anonymous_returns_http_403(
        self,
    ):
        """test_anonymous_returns_http_403

        Returns:

        """
        response = RequestMock.do_request_post(
            xslt_views.XslTransformationTransform.as_view(),
            None,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("core_main_app.components.xsl_transformation.api.xsl_transform")
    @patch.object(TransformSerializer, "validated_data")
    @patch.object(TransformSerializer, "is_valid")
    @patch.object(TransformSerializer, "data")
    def test_is_authenticated_returns_http_200(
        self,
        transform_xsl_serializer_data,
        transform_xsl_serializer_is_valid,
        transform_xsl_serializer_validated_data,
        xslt_transform,
    ):
        """test_is_authenticated_returns_http_200

        Args:
            transform_xsl_serializer_data:
            transform_xsl_serializer_is_valid:
            transform_xsl_serializer_validated_data:
            xslt_transform:

        Returns:

        """
        xslt_transform.return_value = {}
        transform_xsl_serializer_is_valid.return_value = {}
        transform_xsl_serializer_validated_data.return_value = {}
        transform_xsl_serializer_data.return_value = True

        response = RequestMock.do_request_post(
            xslt_views.XslTransformationTransform.as_view(),
            create_mock_user("1", is_anonymous=False),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.xsl_transformation.api.xsl_transform")
    @patch.object(TransformSerializer, "validated_data")
    @patch.object(TransformSerializer, "is_valid")
    @patch.object(TransformSerializer, "data")
    def test_is_staff_returns_http_200(
        self,
        transform_xsl_serializer_data,
        transform_xsl_serializer_is_valid,
        transform_xsl_serializer_validated_data,
        xslt_transform,
    ):
        """test_is_staff_returns_http_200

        Args:
            transform_xsl_serializer_data:
            transform_xsl_serializer_is_valid:
            transform_xsl_serializer_validated_data:
            xslt_transform:

        Returns:

        """
        xslt_transform.return_value = {}
        transform_xsl_serializer_is_valid.return_value = {}
        transform_xsl_serializer_validated_data.return_value = {}
        transform_xsl_serializer_data.return_value = True

        response = RequestMock.do_request_post(
            xslt_views.XslTransformationTransform.as_view(),
            create_mock_user("1", is_staff=True),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
