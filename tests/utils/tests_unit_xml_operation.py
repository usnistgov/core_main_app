""" Xml operation test class
"""
from collections import OrderedDict
from unittest import TestCase

from core_main_app.commons import exceptions
from core_main_app.utils.xml import (
    raw_xml_to_dict,
    remove_lists_from_xml_dict,
    get_content_by_xpath,
    format_content_xml,
)


class TestRawToDict(TestCase):
    """Test raw_xml_to_dict"""

    def test_raw_to_dict_valid(self):
        """Test valid xml

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", "Hello")]))]
        )

        # Act
        xml_dict = raw_xml_to_dict(raw_xml)

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_throws_exception_when_invalid_xml(self):
        """Test invalid xml

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            raw_xml_to_dict(raw_xml)

    def test_raw_to_dict_without_post_processor(self):
        """Test without post processor

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", "1"])]))]
        )

        # Act
        xml_dict = raw_xml_to_dict(raw_xml, postprocessor=None)

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_numeric_post_processor(self):
        """Test with numeric post processor

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", 1])]))]
        )

        # Act
        xml_dict = raw_xml_to_dict(raw_xml, postprocessor="NUMERIC")

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_numeric_and_string_post_processor(self):
        """Test with numeric and string post processor

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", ("1", 1)])]))]
        )

        # Act
        xml_dict = raw_xml_to_dict(raw_xml, postprocessor="NUMERIC_AND_STRING")

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_callable_post_processor(self):
        """Test with a callable post processor

        Returns:

        """

        def test_processor(path, key, value):
            return key, "test"

        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict([("root", "test")])

        # Act
        xml_dict = raw_xml_to_dict(raw_xml, postprocessor=test_processor)

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_unknown_string_raises_error(self):
        """Test with unknown post processor name

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.CoreError):
            raw_xml_to_dict(raw_xml, postprocessor="bad_processor")

    def test_raw_to_dict_with_bad_type_raises_error(self):
        """Test with invalid processor type

        Returns:

        """
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.CoreError):
            raw_xml_to_dict(raw_xml, postprocessor=1)


class TestRemoveListsFromXmlDict(TestCase):
    """Test remove_lists_from_xml_dict"""

    def test_remove_lists_from_xml_dict_empty_dict_does_nothing(self):
        """Test remove lists from xml dict empty dict does nothing

        Returns:

        """
        # Arrange
        xml_dict = {}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertEqual(xml_dict, {})

    def test_remove_lists_from_xml_dict_root_list_is_removed(self):
        """Test remove lists from xml dict root list is removed

        Returns:

        """
        # Arrange
        xml_dict = {"list": [{"value": 1}, {"value": 2}]}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertEqual(xml_dict, {})

    def test_remove_lists_from_xml_dict_root_list_is_not_removed_if_smaller_than_max_size(
        self,
    ):
        """Test remove lists from xml dict root list is not removed if smaller than max size

        Returns:

        """
        # Arrange
        xml_dict = {"list": [{"value": 1}, {"value": 2}]}
        # Act
        remove_lists_from_xml_dict(xml_dict, 3)
        # Assert
        self.assertTrue(xml_dict == {"list": [{"value": 1}, {"value": 2}]})

    def test_remove_lists_from_xml_dict_sub_element_list_is_removed(self):
        """Test remove lists from xml dict sub element list is removed

        Returns:

        """
        # Arrange
        xml_dict = {"root": {"list": [{"value": 1}, {"value": 2}]}}
        # Act
        remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertTrue(xml_dict == {"root": {}})

    def test_remove_lists_from_xml_dict_sub_element_list_is_not_removed_if_smaller_than_max_size(
        self,
    ):
        """Test remove lists from xml dict sub element list is not removed if smaller than max size

        Returns:

        """
        # Arrange
        xml_dict = {"root": {"list": [{"value": 1}, {"value": 2}]}}
        # Act
        remove_lists_from_xml_dict(xml_dict, 3)
        # Assert
        self.assertTrue(
            xml_dict == {"root": {"list": [{"value": 1}, {"value": 2}]}}
        )

    def test_remove_lists_from_xml_dict_sub_elements_only_list_is_removed(
        self,
    ):
        """Test remove lists from xml dict sub elements only list is removed

        Returns:

        """
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
            xml_dict
            == {"root": {"int": 3, "str": "test", "dict": {"value": "test"}}}
        )


class TestGetContentByXpath(TestCase):
    """Test get_content_by_xpath"""

    def test_get_content_and_path_exists(self):
        """test get content and path exists

        Returns:

        """
        # Arrange
        raw_xml = "<root><element>Hello</element></root>"
        # Act
        content = get_content_by_xpath(raw_xml, "/root/element")
        # Assert
        self.assertEqual(content, ["<element>Hello</element>"])

    def test_get_content_path_does_not_exist(self):
        """test get content path does not exist

        Returns:

        """
        # Arrange
        raw_xml = "<root><element>Hello</element></root>"
        # Act
        content = get_content_by_xpath(raw_xml, "/root/test")
        # Assert
        self.assertEqual(content, [])

    def test_get_content_path_found_more_than_once(self):
        """test get content path found more than once

        Returns:

        """
        # Arrange
        raw_xml = (
            "<root><element>Hello</element><element>World</element></root>"
        )
        # Act
        content = get_content_by_xpath(raw_xml, "/root/element")
        # Assert
        self.assertEqual(
            content, ["<element>Hello</element>", "<element>World</element>"]
        )

    def test_get_content_path_is_root(self):
        """test get content path is root

        Returns:

        """
        # Arrange
        raw_xml = "<root><element>Hello</element></root>"
        # Act
        content = get_content_by_xpath(raw_xml, "/root")
        # Assert
        self.assertEqual(content, [raw_xml])

    def test_get_content_path_with_namespace(self):
        """test get content path with namespace

        Returns:

        """
        # Arrange
        raw_xml = """<root xmlns:h="http://www.w3.org/TR/html4/">
        <h:table>
          <h:tr>
            <h:td>Apples</h:td>
            <h:td>Bananas</h:td>
          </h:tr>
        </h:table>
        </root>"""
        # Act
        content = get_content_by_xpath(
            raw_xml,
            "/root/h:table/h:tr/h:td",
            namespaces={"h": "http://www.w3.org/TR/html4/"},
        )
        # Assert
        self.assertEqual(
            content,
            [
                '<h:td xmlns:h="http://www.w3.org/TR/html4/">Apples</h:td>',
                '<h:td xmlns:h="http://www.w3.org/TR/html4/">Bananas</h:td>',
            ],
        )

    def test_get_attribute_path_with_namespace(self):
        """test get attribute path with namespace

        Returns:

        """
        # Arrange
        raw_xml = """<root xmlns:h="http://www.w3.org/TR/html4/">
        <h:table>
          <h:tr class="test">
            <h:td>Apples</h:td>
            <h:td>Bananas</h:td>
          </h:tr>
        </h:table>
        </root>"""
        # Act
        content = get_content_by_xpath(
            raw_xml,
            "/root/h:table/h:tr/@class",
            namespaces={"h": "http://www.w3.org/TR/html4/"},
        )
        # Assert
        self.assertEqual(
            content,
            ["test"],
        )

    def test_get_list_attribute_path_with_namespace(self):
        """test get list attribute path with namespace

        Returns:

        """
        # Arrange
        raw_xml = """<root xmlns:h="http://www.w3.org/TR/html4/">
        <h:table>
          <h:tr>
            <h:td class="class1">Apples</h:td>
            <h:td class="class2">Bananas</h:td>
          </h:tr>
        </h:table>
        </root>"""
        # Act
        content = get_content_by_xpath(
            raw_xml,
            "/root/h:table/h:tr/h:td/@class",
            namespaces={"h": "http://www.w3.org/TR/html4/"},
        )
        # Assert
        self.assertEqual(
            content,
            ["class1", "class2"],
        )

    def test_get_content_returns_list(self):
        """test get content returns list

        Returns:

        """
        # Arrange
        raw_xml = """<root xmlns:h="http://www.w3.org/TR/html4/">
        <h:table>
          <h:tr>
            <h:td>Apples</h:td>
            <h:td>Bananas</h:td>
          </h:tr>
        </h:table>
        </root>"""
        # Act
        content = get_content_by_xpath(
            raw_xml,
            "/root/h:table/h:tr/h:td",
            namespaces={"h": "http://www.w3.org/TR/html4/"},
        )
        # Assert
        self.assertEqual(
            content,
            [
                '<h:td xmlns:h="http://www.w3.org/TR/html4/">Apples</h:td>',
                '<h:td xmlns:h="http://www.w3.org/TR/html4/">Bananas</h:td>',
            ],
        )


class TestFormatContentXml(TestCase):
    """Test Format Content Xml"""

    def test_format_valid_content_xml_returns_content_formatted(self):
        """test_format_valid_content_xml_returns_content_formatted"""

        # Arrange
        xml_string = "<root><test>Hello</test><test>1</test></root>"
        expected_result = (
            "<root>\n  <test>Hello</test>\n  <test>1</test>\n</root>\n"
        )

        # Act
        content = format_content_xml(xml_string)

        # Assert
        self.assertEqual(content, expected_result)

    def test_format_invalid_content_xml_raises_error(self):
        """test_format_invalid_content_xml_raises_error"""

        # Arrange
        xml_string = "<root><test>Hello</test?</root>"

        # Assert
        with self.assertRaises(exceptions.XMLError):
            format_content_xml(xml_string)
