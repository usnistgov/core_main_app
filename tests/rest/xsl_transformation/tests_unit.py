"""Unit tests for xsl transformation rest api
"""
import unittest
from unittest.mock import patch

from django.test.testcases import SimpleTestCase
from rest_framework import status

from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.rest.xsl_transformation import views as xsl_views
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestGetAllXslTransformation(SimpleTestCase):
    """TestGetAllXslTransformation"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = None

    @patch.object(XslTransformation, "get_all")
    def test_get_all_xsl_document_returns_status_403_with_no_permission_needed(
        self, mock_get_all
    ):
        """test_get_all_xsl_document_returns_status_403_with_no_permission_needed

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(XslTransformation, "get_all")
    def test_get_all_xsl_document_returns_status_200_with_staff_permission(
        self, mock_get_all
    ):
        """test_get_all_xsl_document_returns_status_200_with_staff_permission

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        user = create_mock_user("0", True)

        # Act
        response = RequestMock.do_request_get(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPostXslTransformation(SimpleTestCase):
    """TestPostXslTransformation"""

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = None

    @patch.object(XslTransformation, "save_object")
    def test_post_xsl_document_returns_status_403_if_user_is_not_admin(
        self, mock_save
    ):
        """test_post_xsl_document_returns_status_403_if_user_is_not_admin

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("Not working on Jenkins")
    @patch.object(XslTransformation, "save_object")
    def test_post_xsl_document_returns_status_400_if_data_are_not_valid_with_admin_user(
        self, mock_save
    ):
        """test_post_xsl_document_returns_status_400_if_data_are_not_valid_with_admin_user

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        user = create_mock_user("0", True, True)

        # Act
        response = RequestMock.do_request_post(
            xsl_views.XslTransformationList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip("Not working on Jenkins")
    @patch.object(XslTransformation, "save_object")
    def test_post_xsl_document_returns_status_201_if_data_are_valid_with_admin_user(
        self, mock_save
    ):
        """test_post_xsl_document_returns_status_201_if_data_are_valid_with_admin_user

        Args:
            mock_save:

        Returns:

        """
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
