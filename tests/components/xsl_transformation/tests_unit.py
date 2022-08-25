""" Test units
"""
from os.path import join, dirname, realpath
from unittest.case import TestCase

from mock.mock import Mock, patch

from xml_utils.html_tree.parser import html_diff as htmldiff
from core_main_app.commons import exceptions
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_main_app.components.xsl_transformation.models import XslTransformation


class TestXslTransformationGet(TestCase):
    """TestXslTransformationGet"""

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transformation_get_return_xsl_transformation(self, mock_get_by_name):
        """test xsl transformation get return xsl transformation

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_xslt = _create_mock_xsl_transformation(
            name="xslt_name", filename="xslt_filename", content="xslt_content"
        )

        mock_get_by_name.return_value = mock_xslt

        # Act
        result = xsl_transformation_api.get_by_name(mock_xslt.name)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transformation_get_raises_exception_if_object_does_not_exists(
        self, mock_get_by_name
    ):
        """test xsl transformation get raises exception if object does not exists

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_unexisting_name = "unexisting_xslt_name"
        mock_get_by_name.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.get_by_name(mock_unexisting_name)


class TestXslTransformationGetById(TestCase):
    """TestXslTransformationGetById"""

    @patch.object(XslTransformation, "get_by_id")
    def test_xsl_transformation_get_by_id_raises_api_error_if_does_not_exisst(
        self, mock_get
    ):
        """test xsl transformation get by id raises api error if does not exisst

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            xsl_transformation_api.get_by_id(1)

    @patch.object(XslTransformation, "get_by_id")
    def test_xsl_transformation_get_by_id_returns_xsl_transformation(self, mock_get):
        """test xsl transformation get by id returns xsl transformation

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_data = _create_mock_xsl_transformation(
            name="xslt_name_1", filename="xslt_filename_1", content="xslt_content_1"
        )
        mock_get.return_value = mock_data

        # Act
        result = xsl_transformation_api.get_by_id(1)

        # Assert
        self.assertIsInstance(result, XslTransformation)


class TestXslTransformationGetAll(TestCase):
    """TestXslTransformationGetAll"""

    @patch.object(XslTransformation, "get_all")
    def test_xsl_transformation_get_all_contains_only_xsl_transformation(
        self, mock_get_all
    ):
        """test xsl transformation get all contains only xsl transformation

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_xslt_1 = _create_mock_xsl_transformation(
            name="xslt_name_1", filename="xslt_filename_1", content="xslt_content_1"
        )

        mock_xslt_2 = _create_mock_xsl_transformation(
            name="xslt_name_2", filename="xslt_filename_2", content="xslt_content_2"
        )

        mock_get_all.return_value = [mock_xslt_1, mock_xslt_2]

        # Act
        result = xsl_transformation_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, XslTransformation) for item in result))


class TestXslTransformationUpsert(TestCase):
    """TestXslTransformationUpsert"""

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_return_xsl_transformation(self, mock_save):
        """test xsl transformation upsert return xsl transformation

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = (
            "<xsl:stylesheet xmlns:xsl='http://www.w3.org/1999/XSL/Transform' version='1.0'> "
            "<xsl:output method='html' indent='yes' encoding='UTF-8' />"
            "<root></root></xsl:stylesheet>"
        )

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act
        result = xsl_transformation_api.upsert(mock_xslt)

        # Assert
        self.assertIsInstance(result, XslTransformation)

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_raises_exception_if_not_well_formatted(
        self, mock_save
    ):
        """test xsl transformation upsert raises exception if not well formatted

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "bad_content"

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.upsert(mock_xslt)

    @patch.object(XslTransformation, "save")
    def test_xsl_transformation_upsert_raises_exception_if_bad_namespace(
        self, mock_save
    ):
        """test xsl transformation upsert raises exception if bad namespace

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        mock_name = "xslt_name"
        mock_filename = "xslt_filename"
        mock_content = "<root></root>"

        mock_xslt = _create_xsl_transformation(
            name=mock_name, filename=mock_filename, content=mock_content
        )

        mock_save.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.upsert(mock_xslt)


class TestXslTransform(TestCase):
    """TestXslTransform"""

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_return_expected_string(self, mock_get_by_name):
        """test xsl transform return expected string

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")
        mock_html_path = join(mock_data_path, "data_transformed.html")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        with open(mock_html_path, "r", encoding="utf-8") as html_file:
            expected_result = html_file.read()

        # Act
        result = xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)
        html_diff = htmldiff(
            result, expected_result
        )  # Computing difference in resulting content

        # Assert
        self.assertNotIn("<ins>", html_diff)
        self.assertNotIn("<del>", html_diff)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_encode_exception(self, mock_get_by_name):
        """test xsl transform raise api error on encode exception

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        # two .encode() in a row will trigger the exception
        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl", content="\u2000".encode("utf-8")
        )

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_malformed_xslt(self, mock_get_by_name):
        """test xsl transform raise api error on malformed xslt

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl", content="mock_malformed_xslt/>"
        )
        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    def test_xsl_transform_raise_api_error_on_malformed_xml(self, mock_get_by_name):
        """test xsl transform raise api error on malformed xml

        Args:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        mock_xml_data = "<tag>Unclosed"

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)

    @patch.object(XslTransformation, "get_by_name")
    @patch("core_main_app.utils.xml.xsl_transform")
    def test_xsl_transform_raise_api_error_on_other_exception(
        self, mock_xsl_transform, mock_get_by_name
    ):
        """test xsl transform raise api error on other exception

        Args:
            mock_xsl_transform:
            mock_get_by_name:

        Returns:

        """
        # Arrange
        mock_data_path = join(dirname(realpath(__file__)), "data")
        mock_xml_path = join(mock_data_path, "data.xml")
        mock_xsl_path = join(mock_data_path, "transform.xsl")

        with open(mock_xml_path, "r", encoding="utf-8") as xml_file:
            mock_xml_data = xml_file.read()

        mock_xslt = _create_mock_xsl_transformation(
            name="mock_xslt", filename="mock_xslt.xsl"
        )

        with open(mock_xsl_path, "r", encoding="utf-8") as xsl_file:
            mock_xslt.content = xsl_file.read()

        mock_get_by_name.return_value = mock_xslt
        mock_xsl_transform.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            xsl_transformation_api.xsl_transform(mock_xml_data, mock_xslt.name)


def _create_mock_xsl_transformation(name=None, filename=None, content=None):
    """create mock xsl transformation

    Args:
        name:
        filename:
        content:

    Returns:

    """
    mock_xslt = Mock(spec=XslTransformation)
    mock_xslt.name = name
    mock_xslt.filename = filename
    mock_xslt.content = content
    return mock_xslt


def _create_xsl_transformation(name=None, filename=None, content=None):
    """create xsl transformation

    Args:
        name:
        filename:
        content:

    Returns:

    """
    xsl_transformation = XslTransformation()
    xsl_transformation.name = name
    xsl_transformation.filename = filename
    xsl_transformation.content = content
    return xsl_transformation
