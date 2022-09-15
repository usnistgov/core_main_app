""" Unit Test TemplateXslRendering
"""
from unittest.case import TestCase

from mock.mock import Mock, patch

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_xsl_rendering import (
    api as template_xsl_rendering_api,
)
from core_main_app.components.template_xsl_rendering.models import TemplateXslRendering
from core_main_app.components.xsl_transformation.models import XslTransformation


class TestTemplateXslRenderingDelete(TestCase):
    """TestTemplateXslRenderingDelete"""

    @patch.object(TemplateXslRendering, "delete")
    def test_delete_template_xsl_rendering_raises_exception_if_error(self, mock_delete):
        """test delete template xsl rendering raises exception if error

        Args:
            mock_delete:

        Returns:

        """
        # Arrange
        template_xsl_rendering = _create_template_xsl_rendering()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            template_xsl_rendering_api.delete(template_xsl_rendering)


class TestTemplateXslRenderingGetById(TestCase):
    """TestTemplateXslRenderingGetById"""

    @patch.object(TemplateXslRendering, "get_by_id")
    def test_get_by_id_returns_object(self, mock_get_by_id):
        """test get by id returns object

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_template_xsl_rendering = _create_mock_template_xsl_rendering()
        mock_template_xsl_rendering.id = 1

        mock_get_by_id.return_value = mock_template_xsl_rendering

        # Act
        result = template_xsl_rendering_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, TemplateXslRendering)

    @patch.object(TemplateXslRendering, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        """test get by id raises exception if object does not exist

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_xsl_rendering_api.get_by_id(mock_absent_id)

    @patch.object(TemplateXslRendering, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(self, mock_get_by_id):
        """test get by id raises exception if internal error

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_xsl_rendering_api.get_by_id(mock_absent_id)


class TestTemplateXslRenderingGetByTemplateId(TestCase):
    """TestTemplateXslRenderingGetByTemplateId"""

    @patch.object(TemplateXslRendering, "get_by_template_id")
    def test_get_by_template_id_returns_object(self, mock_get_by_template_id):
        """test get by template id returns object

        Args:
            mock_get_by_template_id:

        Returns:

        """
        # Arrange
        mock_template_xsl_rendering = _create_mock_template_xsl_rendering()
        template_id = 1

        mock_get_by_template_id.return_value = mock_template_xsl_rendering

        # Act
        result = template_xsl_rendering_api.get_by_template_id(template_id)

        # Assert
        self.assertIsInstance(result, TemplateXslRendering)

    @patch.object(TemplateXslRendering, "get_by_template_id")
    def test_get_by_template_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_template_id
    ):
        """test get by template id raises exception if object does not exist

        Args:
            mock_get_by_template_id:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_template_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_xsl_rendering_api.get_by_template_id(mock_absent_id)

    @patch.object(TemplateXslRendering, "get_by_template_id")
    def test_get_by_template_id_raises_exception_if_internal_error(
        self, mock_get_by_template_id
    ):
        """test get by template id raises exception if internal error

        Args:
            mock_get_by_template_id:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_template_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_xsl_rendering_api.get_by_template_id(mock_absent_id)


class TestTemplateXslRenderingGetByTemplateHash(TestCase):
    """TestTemplateXslRenderingGetByTemplateHash"""

    @patch.object(TemplateXslRendering, "get_by_template_hash")
    def test_get_by_template_hash_returns_object(self, mock_get_by_template_hash):
        """test get by template hash returns object

        Args:
            mock_get_by_template_hash:

        Returns:

        """
        # Arrange
        mock_template_xsl_rendering = _create_mock_template_xsl_rendering()
        mock_get_by_template_hash.return_value = mock_template_xsl_rendering
        template_hash = "fhf7595ddha0d"

        # Act
        result = template_xsl_rendering_api.get_by_template_hash(template_hash)

        # Assert
        self.assertIsInstance(result, TemplateXslRendering)

    @patch.object(TemplateXslRendering, "get_by_template_hash")
    def test_get_by_template_hash_raises_exception_if_object_does_not_exist(
        self, mock_get_by_template_hash
    ):
        """test get by template hash raises exception if object does not exist

        Args:
            mock_get_by_template_hash:

        Returns:

        """
        # Arrange
        mock_absent_hash = "dummy_hash"
        mock_get_by_template_hash.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_xsl_rendering_api.get_by_template_hash(mock_absent_hash)

    @patch.object(TemplateXslRendering, "get_by_template_hash")
    def test_get_by_template_hash_returns_nothing_if_not_templates(
        self, mock_get_by_template_hash
    ):
        """test get by template hash returns nothing if not templates

        Args:
            mock_get_by_template_hash:

        Returns:

        """
        # Arrange
        mock_absent_hash = "dummy_hash"
        mock_get_by_template_hash.return_value = []

        # Act
        result = template_xsl_rendering_api.get_by_template_hash(mock_absent_hash)
        # Assert
        self.assertEqual(len(result), 0)

    @patch.object(TemplateXslRendering, "get_by_template_hash")
    def test_get_by_template_hash_raises_exception_if_internal_error(
        self, mock_get_by_template_hash
    ):
        """test get by template hash raises exception if internal error

        Args:
            mock_get_by_template_hash:

        Returns:

        """
        # Arrange
        mock_absent_hash = "dummy_hash"
        mock_get_by_template_hash.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_xsl_rendering_api.get_by_template_hash(mock_absent_hash)


class TestTemplateXslRenderingGetAll(TestCase):
    """TestTemplateXslRenderingGetAll"""

    @patch.object(TemplateXslRendering, "get_all")
    def test_get_all(self, mock_get_all):
        """test get all

        Args:
            mock_get_all:

        Returns:

        """
        # Arrange
        mock_template_xsl_rendering1 = _create_mock_template_xsl_rendering()
        mock_template_xsl_rendering2 = _create_mock_template_xsl_rendering()

        mock_get_all.return_value = [
            mock_template_xsl_rendering1,
            mock_template_xsl_rendering2,
        ]

        # Act
        result = template_xsl_rendering_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, TemplateXslRendering) for item in result))


def _create_template_xsl_rendering():
    """Mocks an TemplateXslRendering.

    Returns:
        TemplateXslRendering mock.

    """
    template_xsl_rendering = TemplateXslRendering()
    template_xsl_rendering = _set_template_xsl_rendering_fields(template_xsl_rendering)

    return template_xsl_rendering


def _create_mock_template_xsl_rendering():
    """Mocks an TemplateXslRendering.

    Returns:
        TemplateXslRendering mock.

    """
    mock_template_xsl_rendering = Mock(spec=TemplateXslRendering)
    mock_template_xsl_rendering = _set_template_xsl_rendering_fields(
        mock_template_xsl_rendering
    )

    return mock_template_xsl_rendering


def _set_template_xsl_rendering_fields(template_xsl_rendering):
    """Sets TemplateXslRendering fields.

    Returns:
        TemplateXslRendering with assigned fields.

    """
    template_xsl_rendering.template = Template()
    template_xsl_rendering.template.id = 1
    template_xsl_rendering.list_xslt = XslTransformation()
    template_xsl_rendering.detail_xslt = XslTransformation()

    return template_xsl_rendering
