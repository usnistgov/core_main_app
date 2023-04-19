""" Integration Test for Template xsl rendering
"""

from tests.components.template_xsl_rendering.fixtures.fixtures import (
    TemplateXslRenderingFixtures,
)

from core_main_app.commons import exceptions
from core_main_app.components.template_xsl_rendering.models import (
    TemplateXslRendering,
)

from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)

fixture_template_rendering = TemplateXslRenderingFixtures()


class TestTemplateXslRenderingAddOrDelete(IntegrationTransactionTestCase):
    """Test Template Xsl Rendering Add Or Delete"""

    fixture = fixture_template_rendering

    def test_add_or_delete_returns_none_when_nothing_happened(self):
        """test_add_or_delete_returns_none_when_nothing_happened

        Args:

        Returns:

        """

        # Act
        result = template_xsl_rendering_api.add_or_delete(
            self.fixture.template_1,
            list_xslt=None,
            default_detail_xslt=None,
            list_detail_xslt=None,
        )

        # Assert
        self.assertEqual(result, None)

    def test_add_or_delete_with_given_list_xslt_creates_template_xsl_rendering(
        self,
    ):
        """test add or delete with given list xslt creates_template_xsl_rendering

        Args:

        Returns:

        """
        # Arrange
        list_xslt = self.fixture.xsl_transformation_1

        # Act
        result = template_xsl_rendering_api.add_or_delete(
            self.fixture.template_3,
            list_xslt=list_xslt,
            default_detail_xslt=None,
            list_detail_xslt=None,
        )

        # Assert
        self.assertTrue(isinstance(result, TemplateXslRendering))
        self.assertEqual(result.list_xslt, list_xslt)

    def test_add_or_delete_with_given_list_detail_xslt_creates_template_xsl_rendering(
        self,
    ):
        """test add or delete with given list detail xslt creates_template_xsl_rendering

        Args:

        Returns:

        """
        # Arrange
        list_detail_xslt = [self.fixture.xsl_transformation_1]

        # Act
        result = template_xsl_rendering_api.add_or_delete(
            self.fixture.template_3,
            list_xslt=None,
            default_detail_xslt=None,
            list_detail_xslt=list_detail_xslt,
        )

        # Assert
        self.assertTrue(isinstance(result, TemplateXslRendering))

    def test_add_or_delete_with_wrong_template_xsl_id_raises_api_error(self):
        """test add or delete with wrong template xsl id raises api error

        Args:

        Returns:

        """

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            template_xsl_rendering_api.add_or_delete(
                self.fixture.template_3,
                list_xslt=None,
                default_detail_xslt=None,
                list_detail_xslt=None,
                template_xsl_rendering_id=-1,
            )

    def test_add_or_delete_xslt_updates_template_xsl_rendering(
        self,
    ):
        """test add or delete with given list detail xslt creates_template_xsl_rendering

        Args:

        Returns:

        """

        # Act
        result = template_xsl_rendering_api.add_or_delete(
            self.fixture.template_2,
            list_xslt=self.fixture.xsl_transformation_1,
            default_detail_xslt=None,
            list_detail_xslt=None,
            template_xsl_rendering_id=self.fixture.template_xsl_rendering_1.id,
        )

        # Assert
        self.assertTrue(isinstance(result, TemplateXslRendering))

    def test_add_or_delete_deletes_template_xsl_rendering(self):
        """test add or delete with given list detail xslt creates_template_xsl_rendering

        Args:

        Returns:

        """
        template_xsl = self.fixture.template_xsl_rendering_1
        # Act
        template_xsl_rendering_api.add_or_delete(
            self.fixture.template_3,
            list_xslt=None,
            default_detail_xslt=None,
            list_detail_xslt=None,
            template_xsl_rendering_id=template_xsl.id,
        )


class TestTemplateXslRenderingAddDetailXslt(IntegrationTransactionTestCase):
    """Test Template Xsl Rendering Add Detail Xslt"""

    fixture = fixture_template_rendering

    def test_template_xsl_add_detail_xslt_raises_error_when_already_exist_in_detail_list(
        self,
    ):
        """test template xsl add detail xslt raises error already exist in detail list

        Args:

        Returns:

        """

        # Act
        with self.assertRaises(Exception):
            template_xsl_rendering_api.add_detail_xslt(
                self.fixture.template_xsl_rendering_2,
                self.fixture.xsl_transformation_3,
            )

    def test_template_xsl_add_detail_xslt(self):
        """test template xsl add detail xslt

        Args:

        Returns:

        """

        # Act
        template_xsl_rendering_api.add_detail_xslt(
            self.fixture.template_xsl_rendering_1,
            self.fixture.xsl_transformation_1,
        )

        # Assert
        self.assertTrue(
            self.fixture.xsl_transformation_1
            in self.fixture.template_xsl_rendering_1.list_detail_xslt.all()
        )


class TestTemplateXslRenderingDeleteDetailXslt(IntegrationTransactionTestCase):
    """Test Template Xsl Rendering Delete Detail Xslt"""

    fixture = fixture_template_rendering

    def test_template_xsl_delete_detail_xslt_raises_error_when_xslt_is_not_in_detail_list(
        self,
    ):
        """test template xsl delete detail xslt raises error when xslt is not in detail list

        Args:

        Returns:

        """

        # Act
        with self.assertRaises(Exception):
            template_xsl_rendering_api.delete_detail_xslt(
                self.fixture.template_xsl_rendering_1,
                self.fixture.xsl_transformation_3,
            )

    def test_template_xsl_delete_detail_xslt_removes_xslt_from_detail_list(
        self,
    ):
        """test template xsl delete detail xslt removes xslt from detail list

        Args:

        Returns:

        """

        # Act
        template_xsl_rendering_api.delete_detail_xslt(
            self.fixture.template_xsl_rendering_2,
            self.fixture.xsl_transformation_3,
        )

        # Assert
        self.assertTrue(
            self.fixture.xsl_transformation_3
            not in self.fixture.template_xsl_rendering_2.list_detail_xslt.all()
        )


class TestTemplateXslRenderingSetDefaultDetailXslt(
    IntegrationTransactionTestCase
):
    """Test Template Xsl Rendering Set Default Detail Xslt"""

    fixture = fixture_template_rendering

    def test_template_xsl_set_default_detail_xslt_raises_error_when_xslt_is_not_in_detail_list(
        self,
    ):
        """test template xsl set default detail xslt raises error when xslt is not in detail list

        Args:

        Returns:

        """

        # Act
        with self.assertRaises(Exception):
            template_xsl_rendering_api.set_default_detail_xslt(
                self.fixture.template_xsl_rendering_1,
                self.fixture.xsl_transformation_3,
            )

    def test_template_xsl_set_default_detail_xslt_adds_xslt_as_default(self):
        """test template xsl set default detail xslt adds xslt as default

        Args:

        Returns:

        """

        # Act
        template_xsl_rendering_api.set_default_detail_xslt(
            self.fixture.template_xsl_rendering_2,
            self.fixture.xsl_transformation_3,
        )

        # Assert
        self.assertEqual(
            self.fixture.xsl_transformation_3,
            self.fixture.template_xsl_rendering_2.default_detail_xslt,
        )
