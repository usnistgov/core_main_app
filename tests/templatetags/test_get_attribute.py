""" Unit tests of get_attribute templatetag
"""
from unittest.case import TestCase

from core_main_app.templatetags.get_attribute import get_attribute


class TestObject:
    """Test object"""

    test = "test"


class TestGetAttribute(TestCase):
    """Test get_attribute"""

    def test_get_attribute_of_empty_object(self):
        """Get attribute of empty object

        Returns:

        """
        result = get_attribute({}, "test")
        self.assertEqual(result, "")

    def test_get_attribute_of_none(self):
        """Get attribute of None

        Returns:

        """
        result = get_attribute(None, "test")
        self.assertEqual(result, "")

    def test_get_attribute_of_object(self):
        """Get attribute of test object

        Returns:

        """
        test_obj = TestObject()
        result = get_attribute(test_obj, "test")
        self.assertEqual(result, "test")

    def test_get_attribute_of_dict(self):
        """Get attribute of dict

        Returns:

        """
        test_dict = {"test": "test"}
        result = get_attribute(test_dict, "test")
        self.assertEqual(result, "test")

    def test_get_attribute_of_list(self):
        """Get attribute of list

        Returns:

        """
        test_tab = ["test"]
        result = get_attribute(test_tab, "0")
        self.assertEqual(result, "test")
