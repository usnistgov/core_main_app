""" Unit tests for `core_main_app.utils.xml` package.
"""

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from core_main_app.commons import exceptions
from core_main_app.utils import xml as xml_utils
from xml_utils.commons import constants as xml_utils_constants


class TestRawXmlToDict(TestCase):
    """Unit tests for `raw_xml_to_dict` function."""

    def test_raw_to_dict_valid(self):
        """Test valid xml"""
        # Arrange
        raw_xml = "<root><test>Hello</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", "Hello")]))]
        )

        # Act
        xml_dict = xml_utils.raw_xml_to_dict(raw_xml)

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_throws_exception_when_invalid_xml(self):
        """Test invalid xml"""
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            xml_utils.raw_xml_to_dict(raw_xml)

    def test_raw_to_dict_without_post_processor(self):
        """Test without post processor"""
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", "1"])]))]
        )

        # Act
        xml_dict = xml_utils.raw_xml_to_dict(raw_xml, postprocessor=None)

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_numeric_post_processor(self):
        """Test with numeric post processor"""
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", 1])]))]
        )

        # Act
        xml_dict = xml_utils.raw_xml_to_dict(raw_xml, postprocessor="NUMERIC")

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_numeric_and_string_post_processor(self):
        """Test with numeric and string post processor"""
        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict(
            [("root", OrderedDict([("test", ["Hello", ("1", 1)])]))]
        )

        # Act
        xml_dict = xml_utils.raw_xml_to_dict(
            raw_xml, postprocessor="NUMERIC_AND_STRING"
        )

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_callable_post_processor(self):
        """Test with a callable post processor"""

        def test_processor(path, key, value):
            return key, "test"

        # Arrange
        raw_xml = "<root><test>Hello</test><test>1</test></root>"
        expected_dict = OrderedDict([("root", "test")])

        # Act
        xml_dict = xml_utils.raw_xml_to_dict(
            raw_xml, postprocessor=test_processor
        )

        # Assert
        self.assertEqual(expected_dict, xml_dict)

    def test_raw_to_dict_with_unknown_string_raises_error(self):
        """Test with unknown post processor name"""
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.CoreError):
            xml_utils.raw_xml_to_dict(raw_xml, postprocessor="bad_processor")

    def test_raw_to_dict_with_bad_type_raises_error(self):
        """Test with invalid processor type"""
        # Arrange
        raw_xml = "<root><test>Hello</test?</root>"

        # Act # Assert
        with self.assertRaises(exceptions.CoreError):
            xml_utils.raw_xml_to_dict(raw_xml, postprocessor=1)


class TestRemoveListsFromXmlDict(TestCase):
    """Test remove_lists_from_xml_dict"""

    def test_remove_lists_from_xml_dict_empty_dict_does_nothing(self):
        """Test remove lists from xml dict empty dict does nothing

        Returns:

        """
        # Arrange
        xml_dict = {}
        # Act
        xml_utils.remove_lists_from_xml_dict(xml_dict)
        # Assert
        self.assertEqual(xml_dict, {})

    def test_remove_lists_from_xml_dict_root_list_is_removed(self):
        """Test remove lists from xml dict root list is removed

        Returns:

        """
        # Arrange
        xml_dict = {"list": [{"value": 1}, {"value": 2}]}
        # Act
        xml_utils.remove_lists_from_xml_dict(xml_dict)
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
        xml_utils.remove_lists_from_xml_dict(xml_dict, 3)
        # Assert
        self.assertTrue(xml_dict == {"list": [{"value": 1}, {"value": 2}]})

    def test_remove_lists_from_xml_dict_sub_element_list_is_removed(self):
        """Test remove lists from xml dict sub element list is removed

        Returns:

        """
        # Arrange
        xml_dict = {"root": {"list": [{"value": 1}, {"value": 2}]}}
        # Act
        xml_utils.remove_lists_from_xml_dict(xml_dict)
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
        xml_utils.remove_lists_from_xml_dict(xml_dict, 3)
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
        xml_utils.remove_lists_from_xml_dict(xml_dict)
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
        content = xml_utils.get_content_by_xpath(raw_xml, "/root/element")
        # Assert
        self.assertEqual(content, ["<element>Hello</element>"])

    def test_get_content_path_does_not_exist(self):
        """test get content path does not exist

        Returns:

        """
        # Arrange
        raw_xml = "<root><element>Hello</element></root>"
        # Act
        content = xml_utils.get_content_by_xpath(raw_xml, "/root/test")
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
        content = xml_utils.get_content_by_xpath(raw_xml, "/root/element")
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
        content = xml_utils.get_content_by_xpath(raw_xml, "/root")
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
        content = xml_utils.get_content_by_xpath(
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
        content = xml_utils.get_content_by_xpath(
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
        content = xml_utils.get_content_by_xpath(
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
        content = xml_utils.get_content_by_xpath(
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
        content = xml_utils.format_content_xml(xml_string)

        # Assert
        self.assertEqual(content, expected_result)

    def test_format_invalid_content_xml_raises_error(self):
        """test_format_invalid_content_xml_raises_error"""

        # Arrange
        xml_string = "<root><test>Hello</test?</root>"

        # Assert
        with self.assertRaises(exceptions.XMLError):
            xml_utils.format_content_xml(xml_string)


class TestUpdateDependencies(TestCase):
    """Unit tests for `update_dependencies` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs: dict[str, any] = {
            "xsd_string": MagicMock(),
            "dependencies": MagicMock(),
        }
        self.mock_xsd_built_tree = MagicMock()

    @patch.object(xml_utils, "XSDTree")
    def test_build_tree_called(self, mock_xsd_tree):
        """test_build_tree_called"""
        xml_utils.update_dependencies(**self.mock_kwargs)
        mock_xsd_tree.build_tree.assert_called_with(
            self.mock_kwargs["xsd_string"]
        )

    @patch.object(xml_utils, "XSDTree")
    def test_find_all_called_for_imports_and_includes(self, mock_xsd_tree):
        """test_find_all_called_for_imports_and_includes"""
        mock_xsd_tree.build_tree.return_value = self.mock_xsd_built_tree
        xml_utils.update_dependencies(**self.mock_kwargs)

        self.mock_xsd_built_tree.findall.assert_has_calls(
            [
                call(f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}import"),
                call(f"{xml_utils_constants.LXML_SCHEMA_NAMESPACE}include"),
            ]
        )

    @patch.object(xml_utils, "XSDTree")
    @patch.object(xml_utils, "_get_schema_location_uri")
    def test_get_schema_location_uri_called_with_imports_and_includes(
        self, mock_get_schema_location_uri, mock_xsd_tree
    ):
        """test_get_schema_location_uri_called_with_imports_and_includes"""
        imported_schema = MagicMock()
        imported_schema_location = MagicMock()
        imported_schema.attrib = {"schemaLocation": imported_schema_location}
        imported_schema_id = MagicMock()

        included_schema = MagicMock()
        included_schema_location = MagicMock()
        included_schema.attrib = {"schemaLocation": included_schema_location}
        included_schema_id = MagicMock()

        mock_get_schema_location_uri.return_value = MagicMock()
        mock_xsd_tree.build_tree.return_value = self.mock_xsd_built_tree

        self.mock_kwargs["dependencies"] = {
            imported_schema_location: imported_schema_id,
            included_schema_location: included_schema_id,
        }

        self.mock_xsd_built_tree.findall.side_effect = [
            [imported_schema],
            [included_schema],
        ]

        xml_utils.update_dependencies(**self.mock_kwargs)
        mock_get_schema_location_uri.assert_has_calls(
            [call(imported_schema_id), call(included_schema_id)]
        )

    @patch.object(xml_utils, "XSDTree")
    @patch.object(xml_utils, "_get_schema_location_uri")
    def test_get_schema_location_uri_not_called_with_empty_dependency_id(
        self, mock_get_schema_location_uri, mock_xsd_tree
    ):
        """test_get_schema_location_uri_not_called_with_empty_dependency_id"""
        imported_schema = MagicMock()
        imported_schema_location = MagicMock()
        imported_schema.attrib = {"schemaLocation": imported_schema_location}

        mock_get_schema_location_uri.return_value = MagicMock()
        mock_xsd_tree.build_tree.return_value = self.mock_xsd_built_tree

        self.mock_kwargs["dependencies"] = {
            imported_schema_location: None,
        }

        self.mock_xsd_built_tree.findall.side_effect = [[imported_schema], []]

        xml_utils.update_dependencies(**self.mock_kwargs)
        mock_get_schema_location_uri.assert_not_called()

    @patch.object(xml_utils, "XSDTree")
    def test_returns_xsd_tree(self, mock_xsd_tree):
        """test_returns_xsd_tree_with_no_dependencies"""
        mock_xsd_tree.build_tree.return_value = self.mock_xsd_built_tree
        self.assertEqual(
            xml_utils.update_dependencies(**self.mock_kwargs),
            self.mock_xsd_built_tree,
        )
