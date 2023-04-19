""" Integration Test for TemplateXslRendering Rest API
"""

from rest_framework import status
from tests.components.template_xsl_rendering.fixtures.fixtures import (
    TemplateXslRenderingFixtures,
)

from core_main_app.rest.template_xsl_rendering import views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

fixture_template_xsl_rendering = TemplateXslRenderingFixtures()


class TestTemplateXslRenderingAddDetailXslt(IntegrationBaseTestCase):
    """TestTemplateXslRenderingAddDetailXslt"""

    fixture = fixture_template_xsl_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_add_detail_xslt_empty_list(self):
        """test_add_detail_xslt_empty_list

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_1.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["default_detail_xslt"],
            self.fixture.xsl_transformation_1.id,
        )
        self.assertIn(
            self.fixture.xsl_transformation_1.id,
            response.data["list_detail_xslt"],
        )

    def test_add_detail_xslt(self):
        """test_add_detail_xslt

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            response.data["default_detail_xslt"],
            str(self.fixture.xsl_transformation_1.id),
        )
        self.assertEqual(len(response.data["list_detail_xslt"]), 2)
        self.assertIn(
            self.fixture.xsl_transformation_1.id,
            response.data["list_detail_xslt"],
        )

    def test_add_detail_xslt_if_object_does_not_exist(self):
        """test_add_detail_xslt_if_object_does_not_exist

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": "5f0fb6aed26ebcc001eb0bf9",
            },
        )

        # Assert

        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestTemplateXslRenderingSetDefaultDetailXslt(IntegrationBaseTestCase):
    """TestTemplateXslRenderingSetDefaultDetailXslt"""

    fixture = fixture_template_xsl_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_set_default_detail_xslt_exists_in_list(self):
        """test_set_default_detail_xslt_exists_in_list

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingSetDefaultDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            str(response.data["default_detail_xslt"]),
            str(self.fixture.xsl_transformation_1.id),
        )

    def test_set_default_detail_xslt_if_object_does_not_exist(self):
        """test_set_default_detail_xslt_if_object_does_not_exist

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingSetDefaultDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": "5f0fb6aed26ebcc001eb0bf9",
            },
        )

        # Assert

        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestTemplateXslRenderingRemoveDetailXslt(IntegrationBaseTestCase):
    """TestTemplateXslRenderingRemoveDetailXslt"""

    fixture = fixture_template_xsl_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_remove_detail_xslt(self):
        """test_remove_detail_xslt

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingRemoveDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(
            str(self.fixture.xsl_transformation_1.id),
            response.data["list_detail_xslt"],
        )
        self.assertEqual(len(response.data["list_detail_xslt"]), 1)

    def test_remove_last_detail_xslt_in_list(self):
        """test_remove_last_detail_xslt_in_list

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingRemoveDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_3.id),
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["default_detail_xslt"])
        self.assertEqual(response.data["list_detail_xslt"], [])

    def test_remove_default_detail_xslt(self):
        """test_remove_default_detail_xslt

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        RequestMock.do_request_patch(
            views.TemplateXslRenderingAddDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_1.id),
            },
        )

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingRemoveDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": str(self.fixture.xsl_transformation_3.id),
            },
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            str(response.data["default_detail_xslt"]),
            str(self.fixture.xsl_transformation_1.id),
        )
        self.assertNotIn(
            str(self.fixture.xsl_transformation_3.id),
            response.data["list_detail_xslt"],
        )
        self.assertNotEqual(response.data["list_detail_xslt"], [])

    def test_remove_if_object_does_not_exist(self):
        """test_remove_if_object_does_not_exist

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingRemoveDetailXslt.as_view(),
            user,
            param={
                "pk": str(self.fixture.template_xsl_rendering_2.id),
                "xslt_id": "5f0fb6aed26ebcc001eb0bf9",
            },
        )

        # Assert

        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class TestTemplateXslRenderingSetListDetailXslt(IntegrationBaseTestCase):
    """TestTemplateXslRenderingSetListDetailXslt"""

    fixture = fixture_template_xsl_rendering

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        self.data = {"ids": []}

    def test_set_empty_list_detail_xslt(self):
        """test_set_empty_list_detail_xslt

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingSetListDetailXslt.as_view(),
            user,
            param={"pk": str(self.fixture.template_xsl_rendering_2.id)},
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["default_detail_xslt"])
        self.assertEqual(response.data["list_detail_xslt"], [])

    def test_set_list_detail_xslt(self):
        """test_set_list_detail_xslt

        Returns:

        """
        # Arrange
        user = create_mock_user("1")
        self.data.update(
            {
                "ids": [
                    str(self.fixture.xsl_transformation_1.id),
                    str(self.fixture.xsl_transformation_2.id),
                ]
            }
        )

        # Act
        response = RequestMock.do_request_patch(
            views.TemplateXslRenderingSetListDetailXslt.as_view(),
            user,
            param={"pk": str(self.fixture.template_xsl_rendering_2.id)},
            data=self.data,
        )

        # Assert

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            str(response.data["default_detail_xslt"]),
            str(self.fixture.xsl_transformation_1.id),
        )
        self.assertEqual(len(response.data["list_detail_xslt"]), 2)
        self.assertIn(
            str(self.fixture.xsl_transformation_1.id),
            str(response.data["list_detail_xslt"]),
        )
        self.assertIn(
            str(self.fixture.xsl_transformation_2.id),
            str(response.data["list_detail_xslt"]),
        )
