""" Integration test for data ordering
"""
from tests.components.data.fixtures.fixtures import AccessControlDataFixture

from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)

# FIXME move other tests (from tests_int.py) here
ordering_data_fixture = AccessControlDataFixture()


class TestGetAllByListTemplate(IntegrationBaseTestCase):
    """TestGetAllByListTemplate"""

    fixture = ordering_data_fixture

    def test_get_all_by_list_template_data_ordering(self):
        """test_get_all_by_list_template_data_ordering

        Returns:

        """
        # Arrange
        template = self.fixture.template.id
        ascending_order_by_field = ["+title"]
        descending_order_by_field = ["-title"]
        # Act
        ascending_result = Data.get_all_by_list_template(
            [template], ascending_order_by_field
        )
        descending_result = Data.get_all_by_list_template(
            [template], descending_order_by_field
        )
        # Assert
        for i in range(len(ascending_result)):
            self.assertTrue(
                ascending_result.all()[i].title
                == descending_result.all()[len(ascending_result) - i - 1].title
            )

    def test_get_all_by_list_template_data_ascending_sorting(self):
        """test_get_all_by_list_template_data_ascending_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_field = ["+title"]
        template = self.fixture.template.id
        # Act
        ascending_result = Data.get_all_by_list_template(
            [template], ascending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_1.title == ascending_result.all()[0].title
        )
        self.assertTrue(
            self.fixture.data_2.title == ascending_result.all()[1].title
        )

    def test_get_all_by_list_template_data_descending_sorting(self):
        """test_get_all_by_list_template_data_descending_sorting

        Returns:

        """
        # Arrange
        descending_order_by_field = ["-title"]
        template = self.fixture.template.id
        # Act
        descending_result = Data.get_all_by_list_template(
            [template], descending_order_by_field
        )
        # Assert
        self.assertTrue(
            self.fixture.data_2.title
            == descending_result.all()[len(descending_result) - 2].title
        )
        self.assertTrue(
            self.fixture.data_1.title
            == descending_result.all()[len(descending_result) - 1].title
        )

    def test_get_all_by_list_template_multi_field_sorting(self):
        """test_get_all_by_list_template_multi_field_sorting

        Returns:

        """
        # Arrange
        ascending_order_by_multi_field = ["+template", "+title"]
        descending_order_by_multi_field = ["+template", "-title"]
        template = self.fixture.template.id
        # Act
        ascending_result = Data.get_all_by_list_template(
            [template], ascending_order_by_multi_field
        )
        descending_result = Data.get_all_by_list_template(
            [template], descending_order_by_multi_field
        )
        # Assert
        self.assertEqual(
            self.fixture.data_1.title, ascending_result.all()[0].title
        )
        self.assertEqual(
            self.fixture.data_2.user_id, ascending_result.all()[1].user_id
        )

        self.assertEqual(
            self.fixture.data_2.user_id, descending_result.all()[3].user_id
        )
        self.assertEqual(
            self.fixture.data_1.user_id, descending_result.all()[4].user_id
        )
