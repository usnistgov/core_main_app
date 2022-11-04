""" Tests View Data utils
"""
from unittest import TestCase

from core_main_app.components.data.models import Data
from core_main_app.utils.view_builders.data import _get_data_title


class TestPageTitle(TestCase):
    """Test raw_xml_to_dict"""

    def setUp(self) -> None:
        self.title = "test"

    def test_page_title_set_when_when_in_data(self):
        """test_page_title_set_when_when_in_data

        Returns:

        """
        # Arrange
        data = Data(title=self.title)
        # Act
        data_title = _get_data_title(data)
        # Assert
        self.assertEqual(data_title, self.title)

    def test_page_title_empty_when_not_set_in_data(self):
        """test_page_title_None_when_not_when_in_data

        Returns:

        """
        # Arrange
        data = Data()
        # Act
        data_title = _get_data_title(data)
        # Assert
        self.assertEqual(data_title, "")

    def test_page_title_None_when_not_in_dict(self):
        """test_page_title_None_when_not_in_dict

        Returns:

        """
        # Arrange
        data = {}
        # Act
        data_title = _get_data_title(data)
        # Assert
        self.assertEqual(data_title, None)

    def test_page_title_set_when_in_dict(self):
        """test_page_title_set_when_in_dict

        Returns:

        """
        # Arrange
        data = {"title": self.title}
        # Act
        data_title = _get_data_title(data)
        # Assert
        self.assertEqual(data_title, self.title)

    def test_page_title_None_when_not_data_is_None(self):
        """test_page_title_None_when_not_data_is_None

        Returns:

        """
        # Arrange
        data = None
        # Act
        data_title = _get_data_title(data)
        # Assert
        self.assertEqual(data_title, None)
