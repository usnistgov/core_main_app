from unittest.case import TestCase
from lxml.html.diff import htmldiff
from mock.mock import Mock, patch
from os.path import join, dirname, realpath
from core_main_app.commons.exceptions import MDCSError
from core_main_app.components.xsl_transformation.api import xsl_transformation_get, xsl_transformation_list, \
    xsl_transformation_post, xsl_transform
from core_main_app.components.xsl_transformation.models import XslTransformation


class TestXslTransformationGet(TestCase):

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transformation_get_return_xsl_transformation(self, mock_get_by_name):
        # Arrange
        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "xslt_name"
        mock_xslt.filename = "xslt_filename"
        mock_xslt.content = "xslt_content"

        mock_get_by_name.return_value = mock_xslt

        # Act
        result = xsl_transformation_get(mock_xslt.name)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transformation_get_throws_exception_if_object_does_not_exists(self, mock_get_by_name):
        # Arrange
        mock_unexisting_name = "unexisting_xslt_name"
        mock_get_by_name.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            xsl_transformation_get(mock_unexisting_name)


class TestXslTransformationList(TestCase):

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_all')
    def test_xsl_transformation_list_contains_only_xsl_transformation(self, mock_get_all):
        # Arrange
        mock_xslt_1 = Mock(spec=XslTransformation)
        mock_xslt_1.name = "xslt_name_1"
        mock_xslt_1.filename = "xslt_filename_1"
        mock_xslt_1.content = "xslt_content_1"

        mock_xslt_2 = Mock(spec=XslTransformation)
        mock_xslt_2.name = "xslt_name_2"
        mock_xslt_2.filename = "xslt_filename_2"
        mock_xslt_2.content = "xslt_content_2"

        mock_get_all.return_value = [mock_xslt_1, mock_xslt_2]

        # Act
        result = xsl_transformation_list()

        # Assert
        self.assertTrue(all(isinstance(item, XslTransformation) for item in result))


class TestXslTransformationPost(TestCase):

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.save')
    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transformation_post_new_return_xsl_transformation(self, mock_save, mock_get_by_name):
        # Arrange
        mock_xslt = Mock(spec=XslTransformation)
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "xslt_content"

        mock_xslt.name = mock_name
        mock_xslt.filename = mock_filename
        mock_xslt.content = mock_content

        mock_save.return_value = mock_xslt
        mock_get_by_name.side_effect = Exception()

        # Act
        result = xsl_transformation_post(mock_name, mock_filename, mock_content)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.save')
    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transformation_post_existing_return_xsl_transformation(self, mock_save, mock_get_by_name):
        # Arrange
        mock_xslt = Mock(spec=XslTransformation)
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "xslt_content"

        mock_xslt.name = mock_name
        mock_xslt.filename = mock_filename
        mock_xslt.content = mock_content

        mock_save.return_value = mock_xslt
        mock_get_by_name.return_value = mock_xslt

        # Act
        result = xsl_transformation_post(mock_name, mock_filename, mock_content)

        # Assert
        self.assertIsInstance(result, XslTransformation)


class TestXslTransform(TestCase):

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transform_return_expected_string(self, mock_get_by_name):
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")
        mock_html_path = join(mock_data_path, "data_transformed.html")

        with open(mock_xml_path, "r") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "mock_xslt"
        mock_xslt.filename = "mock_xslt.xsl"

        with open(mock_xsl_path, "r") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        with open(mock_html_path, "r") as html_file:
            expected_result = html_file.read()

        # Act
        result = xsl_transform(mock_xml_data, mock_xslt.name)
        html_diff = htmldiff(result, expected_result)  # Computing difference in resulting content

        # Assert
        self.assertNotIn("<ins>", html_diff)
        self.assertNotIn("<del>", html_diff)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transform_raise_mdcs_error_on_encode_exception(self, mock_get_by_name):
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "mock_xslt"
        mock_xslt.filename = "mock_xslt.xsl"
        mock_xslt.content = u"\u2000".encode("utf-8")  # two .encode() in a row will trigger the exception

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(MDCSError):
            xsl_transform(mock_xml_data, mock_xslt.name)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transform_raise_mdcs_error_on_malformed_xslt(self, mock_get_by_name):
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "mock_xslt"
        mock_xslt.filename = "mock_xslt.xsl"
        mock_xslt.content = "mock_malformed_xslt/>"

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(MDCSError):
            xsl_transform(mock_xml_data, mock_xslt.name)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    def test_xsl_transform_raise_mdcs_error_on_malformed_xml(self, mock_get_by_name):
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        mock_xml_data = "<tag>Unclosed"

        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "mock_xslt"
        mock_xslt.filename = "mock_xslt.xsl"

        with open(mock_xsl_path, "r") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(MDCSError):
            xsl_transform(mock_xml_data, mock_xslt.name)

    @patch('core_main_app.components.xsl_transformation.models.XslTransformation.get_by_name')
    @patch('lxml.etree.fromstring')
    def test_xsl_transform_raise_mdcs_error_on_other_exception(self, mock_etree_fromstring, mock_get_by_name):
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        with open(mock_xml_path, "r") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = Mock(spec=XslTransformation)
        mock_xslt.name = "mock_xslt"
        mock_xslt.filename = "mock_xslt.xsl"

        with open(mock_xsl_path, "r") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt
        mock_etree_fromstring.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(MDCSError):
            xsl_transform(mock_xml_data, mock_xslt.name)
