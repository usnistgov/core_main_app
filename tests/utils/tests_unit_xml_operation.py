"""
    Xml operation test class
"""
from collections import OrderedDict
from unittest import TestCase

import core_main_app.commons.exceptions as exceptions
from core_main_app.utils.xml import raw_xml_to_dict, remove_lists_from_xml_dict


class TestRawToDict(TestCase):
    def test_raw_to_dict_valid(self):
        # Arrange
        raw_xml = "<root><test>Hello</test></root>"
        expected_dict = OrderedDict([("root", OrderedDict([("test", "Hello")]))])

        # Act
        xml_dict = raw_xml_to_dict(raw_xml)

        # Assert
        self.assertEquals(expected_dict, xml_dict)

    def test_raw_to_dict_throws_exception_when_invalid_xml(self):
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            raw_xml_to_dict(raw_xml)


class TestRemoveListsFromXmlDict(TestCase):
    def test_remove_lists_from_xml_dict_empty_dict_does_nothing(self):
        # Arrange
        xml_dict = {}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertTrue(xml_dict == {})

    def test_remove_lists_from_xml_dict_root_list_is_removed(self):
        # Arrange
        xml_dict = {"list": [{"value": 1}, {"value": 2}]}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertTrue(xml_dict == {})

    def test_remove_lists_from_xml_dict_root_list_is_not_removed_if_smaller_than_max_size(
        self,
    ):
        # Arrange
        xml_dict = {"list": [{"value": 1}, {"value": 2}]}
        # Act
        remove_lists_from_xml_dict(xml_dict, 3)
        # Assert
        self.assertTrue(xml_dict == {"list": [{"value": 1}, {"value": 2}]})

    def test_remove_lists_from_xml_dict_sub_element_list_is_removed(self):
        # Arrange
        xml_dict = {"root": {"list": [{"value": 1}, {"value": 2}]}}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertTrue(xml_dict == {"root": {}})

    def test_remove_lists_from_xml_dict_sub_element_list_is_not_removed_if_smaller_than_max_size(
        self,
    ):
        # Arrange
        xml_dict = {"root": {"list": [{"value": 1}, {"value": 2}]}}
        # Act
        remove_lists_from_xml_dict(xml_dict, 3)
        # Assert
        self.assertTrue(xml_dict == {"root": {"list": [{"value": 1}, {"value": 2}]}})

    def test_remove_lists_from_xml_dict_sub_elements_only_list_is_removed(self):
        # Arrange
        xml_dict = {
            "root": {
                "list": [{"value": 1}, {"value": 2}],
                "int": 3,
                "str": "test",
                "dict": {"value": "test"},
            }
        }
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertTrue(
            xml_dict == {"root": {"int": 3, "str": "test", "dict": {"value": "test"}}}
        )
