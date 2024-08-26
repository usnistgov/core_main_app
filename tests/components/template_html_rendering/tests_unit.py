""" Unit Test TemplateHtmlRendering
"""

from unittest.case import TestCase
from unittest.mock import Mock, patch

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_html_rendering import (
    api as template_html_rendering_api,
)
from core_main_app.components.template_html_rendering.models import (
    TemplateHtmlRendering,
)


class TestTemplateHtmlRenderingGetByTemplateId(TestCase):
    """TestTemplateHtmlRenderingGetByTemplateId"""

    @patch.object(TemplateHtmlRendering, "get_by_template_id")
    def test_get_by_template_id_returns_object(self, mock_get_by_template_id):
        """test get by id returns object

        Args:
            mock_get_by_template_id:

        Returns:

        """
        # Arrange
        mock_template_html_rendering = Mock(TemplateHtmlRendering)

        mock_get_by_template_id.return_value = mock_template_html_rendering

        # Act
        result = template_html_rendering_api.get_by_template_id(
            mock_template_html_rendering.id
        )

        # Assert
        self.assertIsInstance(result, TemplateHtmlRendering)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_template_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_template_html_rendering_object
    ):
        """test get by id raises exception if object does not exist

        Args:
            mock_get_by_template_html_rendering_object:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_template_html_rendering_object.get.side_effect = (
            ObjectDoesNotExist()
        )

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_html_rendering_api.get_by_template_id(mock_absent_id)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_template_id_raises_exception_if_model_error(
        self, mock_get_by_template_html_rendering_object
    ):
        """test get by template id raises exception if internal error

        Args:
            mock_get_by_template_html_rendering_object:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_get_by_template_html_rendering_object.get.side_effect = (
            exceptions.ModelError("Error.")
        )

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_html_rendering_api.get_by_template_id(mock_absent_id)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_template_id_raises_model_error_if_exception(
        self, mock_template_html_rendering_objects
    ):
        """test get by template id raises exception if exception

        Args:
            mock_template_html_rendering_objects:

        Returns:

        """
        # Arrange
        mock_template_html_rendering_objects.get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_html_rendering_api.get_by_template_id(1)


class TestTemplateHtmlRenderingGetByTemplateHash(TestCase):
    """TestTemplateHtmlRenderingGetByTemplateHash"""

    @patch.object(TemplateHtmlRendering, "get_by_template_hash")
    def test_get_by_template_hash_returns_object(
        self, mock_get_by_template_hash
    ):
        """test get by template hash returns object

        Args:
            mock_get_by_template_hash:

        Returns:

        """
        # Arrange
        mock_get_by_template_hash.return_value = Mock(TemplateHtmlRendering)
        template_hash = "abcd1234"

        # Act
        result = template_html_rendering_api.get_by_template_hash(
            template_hash
        )

        # Assert
        self.assertIsInstance(result, TemplateHtmlRendering)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_template_hash_raises_exception_if_object_does_not_exist(
        self, mock_get_by_template_html_rendering_object
    ):
        """test get by template hash raises exception if object does not exist

        Args:
            mock_get_by_template_html_rendering_object:

        Returns:

        """
        # Arrange
        mock_absent_hash = "dummy_hash"
        mock_get_by_template_html_rendering_object.get.side_effect = (
            ObjectDoesNotExist()
        )

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_html_rendering_api.get_by_template_hash(mock_absent_hash)

    @patch.object(TemplateHtmlRendering, "get_by_template_hash")
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
        result = template_html_rendering_api.get_by_template_hash(
            mock_absent_hash
        )
        # Assert
        self.assertEqual(len(result), 0)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_template_hash_raises_model_error_if_exception(
        self, mock_template_html_rendering_objects
    ):
        """test get by template id raises exception if exception

        Args:
            mock_template_html_rendering_objects:

        Returns:

        """
        # Arrange
        mock_template_html_rendering_objects.get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_html_rendering_api.get_by_template_hash("abcd")


class TestTemplateHtmlRenderingGetById(TestCase):
    """TestTemplateHtmlRenderingGetById"""

    @patch.object(TemplateHtmlRendering, "get_by_id")
    def test_get_by_id_returns_object(self, mock_get_by_id):
        """test get by id returns object

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_template_html_rendering = Mock(TemplateHtmlRendering)

        mock_get_by_id.return_value = mock_template_html_rendering

        # Act
        result = template_html_rendering_api.get_by_id(
            mock_template_html_rendering.id
        )

        # Assert
        self.assertIsInstance(result, TemplateHtmlRendering)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_template_html_rendering_objects
    ):
        """test get by id raises exception if object does not exist

        Args:
            mock_template_html_rendering_objects:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_template_html_rendering_objects.get.side_effect = (
            ObjectDoesNotExist()
        )

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            template_html_rendering_api.get_by_id(mock_absent_id)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_id_raises_exception_if_model_error(
        self, mock_template_html_rendering_objects
    ):
        """test get by id raises exception if internal error

        Args:
            mock_template_html_rendering_objects:

        Returns:

        """
        # Arrange
        mock_absent_id = -1

        mock_template_html_rendering_objects.get.side_effect = (
            exceptions.ModelError("Error.")
        )

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_html_rendering_api.get_by_id(mock_absent_id)

    @patch.object(TemplateHtmlRendering, "objects")
    def test_get_by_id_raises_model_error_if_exception(
        self, mock_template_html_rendering_objects
    ):
        """test get by template id raises exception if exception

        Args:
            mock_template_html_rendering_objects:

        Returns:

        """
        # Arrange
        mock_template_html_rendering_objects.get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            template_html_rendering_api.get_by_id(1)


class TestTemplateHtmlRenderingGetAll(TestCase):
    """TestTemplateHtmlRenderingGetAll"""

    def test_template_html_rendering_get_all_returns_empty_list(self):
        """test_template_html_rendering_get_all_returns_empty_list"""
        # Act
        result = template_html_rendering_api.get_all()
        # Assert
        self.assertEqual(len(result), 0)

    @patch.object(TemplateHtmlRendering, "get_all")
    def test_template_html_rendering_get_all_returns_list(self, mock_get_all):
        """test_template_html_rendering_get_all_returns_list"""

        # Arrange
        expected_result = [
            Mock(TemplateHtmlRendering),
            Mock(TemplateHtmlRendering),
        ]

        mock_get_all.return_value = expected_result

        # Act
        result = template_html_rendering_api.get_all()
        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(
            all(isinstance(item, TemplateHtmlRendering) for item in result)
        )


class TestTemplateHtmlRenderingUpsert(TestCase):
    """TestTemplateHtmlRenderingUpsert"""

    @patch.object(TemplateHtmlRendering, "save")
    def test_template_html_rendering_creates_bucket(self, mock_save):
        """test_template_html_rendering_returns_no_error"""

        template_html_rendering = Mock(TemplateHtmlRendering)

        mock_save.return_value = template_html_rendering

        template_html_rendering_api.upsert(template_html_rendering)
        self.assertIsInstance(template_html_rendering, TemplateHtmlRendering)


class TestTemplateHtmlRenderingDelete(TestCase):
    """TestTemplateHtmlRenderingDelete"""

    @patch.object(TemplateHtmlRendering, "delete")
    def test_delete_returns_no_error(self, mock_delete):
        """test_delete_returns_no_error"""

        # Arrange
        mock_delete.return_value = None

        # Act # Assert
        self.assertEqual(
            template_html_rendering_api.delete(Mock(TemplateHtmlRendering)),
            None,
        )


class TestTemplateHtmlRenderingStr(TestCase):
    """TestTemplateHtmlRenderingStr"""

    def test_template_html_rendering_str(
        self,
    ):
        """test_template_html_rendering_str

        Args:

        Returns:

        """
        # Arrange
        mock_template_html_rendering = TemplateHtmlRendering()
        mock_template = Template()
        mock_template.display_name = "Template (Version 1)"
        mock_template_html_rendering.template = mock_template

        # Act
        result = str(mock_template_html_rendering)

        # Assert
        self.assertEqual(result, mock_template.display_name)
