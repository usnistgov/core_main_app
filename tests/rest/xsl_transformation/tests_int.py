"""Integration tests for xsl transformation rest api
"""
from bson import ObjectId
from rest_framework import status

import core_main_app.rest.xsl_transformation.views as xsl_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.rest.xsl_transformation.fixtures.fixtures import XslTransformationFixtures

fixture_data = XslTransformationFixtures()


class TestGetAllXslTransformationList(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestGetAllXslTransformationList, self).setUp()

    def test_get_all_returns_status_403_with_no_permission_needed(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPostXslTransformationList(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestPostXslTransformationList, self).setUp()
        self.data = None

    def test_post_returns_status_403_if_user_is_unauthorized(self):
        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_returns_status_400_if_data_are_not_valid_with_admin_user(self):
        # Arrange
        user = create_mock_user("0", True, True)

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_returns_status_201_if_data_are_valid_with_admin_user(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.data = {
            "name": "name",
            "filename": "filename.xsd",
            "content": '<?xml version="1.0" encoding="UTF-8"?>'
            '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">'
            "<xsl:template></xsl:template></xsl:stylesheet>",
        }

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestGetXslTransformationDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestGetXslTransformationDetail, self).setUp()
        self.data = None

    def test_get_returns_object_when_found(self):
        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestDeleteXslTransformationDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestDeleteXslTransformationDetail, self).setUp()
        self.data = None

    def test_delete_raise_403_if_user_is_unauthorized(self):
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_delete(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_delete(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_delete(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_return_204_if_document_is_deleted_whit_success(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        # Act
        response = RequestMock.do_request_delete(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchXslTransformationDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestPatchXslTransformationDetail, self).setUp()
        self.data = None

    def test_patch_raise_403_if_user_is_authorized(self):
        # Arrange
        user = create_mock_user("0")
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_patch(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_raise_404_when_not_found(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": str(ObjectId())}

        # Act
        response = RequestMock.do_request_patch(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_raise_500_sever_error_when_general_error_occured(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": "0"}

        # Act
        response = RequestMock.do_request_patch(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_patch_returns_200_when_data_are_valid_with_authorized_user(self):
        # Arrange
        user = create_mock_user("0", True, True)
        self.param = {"pk": self.fixture.data_1.id}

        self.data = {
            "name": "test_",
            "filename": "test_filename_",
        }

        # Act
        response = RequestMock.do_request_patch(
            xsl_views.XslTransformationDetail.as_view(), user, self.data, self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostXslTransformationTransform(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestPostXslTransformationTransform, self).setUp()
        self.data = None

    def test_post_raise_error_500_if_xslt_does_not_exist(self):
        # Arrange
        user = create_mock_user("0")

        self.data = {
            "xml_content": "xml_content",
            "xslt_name": "xslt_name",
        }

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationTransform.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_return_status_200_if_xml_and_xslt_name_are_valid_parameters(self):
        # Arrange
        user = create_mock_user("0")

        self.data = {
            "xml_content": "<test></test>",
            "xslt_name": "name_1",
        }

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationTransform.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
