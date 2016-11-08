from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template


class TestTemplateGet(TestCase):

    @patch('core_main_app.components.template.models.Template.get_by_id')
    def test_template_get_return_template(self, mock_get_by_id):
        # Arrange
        mock_template = Mock(spec=Template)
        mock_template.filename = "Schema"
        mock_template.content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        mock_template.hash = ""
        mock_template.id = ObjectId()

        mock_get_by_id.return_value = mock_template

        # Act
        result = template_api.get(mock_template.id)

        # Assert
        self.assertIsInstance(result, Template)

    @patch('core_main_app.components.template.models.Template.get_by_id')
    def test_template_get_throws_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            template_api.get(mock_absent_id)


class TestTemplateList(TestCase):
    @patch('core_main_app.components.template.models.Template.get_all')
    def test_template_list_contains_only_template(self, mock_get_all):
        # Arrange
        mock_template1 = Mock(spec=Template)
        mock_template1.filename = "Schema"
        mock_template1.content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        mock_template1.hash = ""

        mock_template2 = Mock(spec=Template)
        mock_template2.filename = "Schema"
        mock_template2.content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        mock_template2.hash = ""

        mock_get_all.return_value = [mock_template1, mock_template2]

        # Act
        result = template_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, Template) for item in result))


class TestTemplateSave(TestCase):

    @patch('core_main_app.components.template.models.Template.save')
    def test_template_create_valid_template(self, mock_save):
        # Arrange
        mock_template = Mock(spec=Template)

        mock_template_filename = "Schema"
        mock_template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        mock_template_hash = ""
        mock_template_id = ObjectId()

        mock_template.filename = mock_template_filename
        mock_template.content = mock_template_content
        mock_template.hash = mock_template_hash
        mock_template.id = mock_template_id

        mock_save.return_value = mock_template

        # Act
        result = template_api.create(mock_template_filename, mock_template_content)

        # Assert
        self.assertIsInstance(result, Template)

    @patch('core_main_app.components.template.models.Template.save')
    def test_template_create_valid_template_with_dependencies(self, mock_save):
        # Arrange
        mock_template = Mock(spec=Template)

        mock_template_filename = "Schema"
        mock_template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        mock_template_hash = ""
        mock_template_dependencies = [ObjectId()]
        mock_template_id = ObjectId()

        mock_template.filename = mock_template_filename
        mock_template.content = mock_template_content
        mock_template.hash = mock_template_hash
        mock_template.id = mock_template_id
        mock_template.dependencies = mock_template_dependencies

        mock_save.return_value = mock_template

        # Act
        result = template_api.create(mock_template_filename, mock_template_content, mock_template_dependencies)

        # Assert
        self.assertIsInstance(result, Template)

    @patch('core_main_app.components.template.models.Template.save')
    def test_template_create_raise_xsd_error_if_invalid(self, mock_save):
        # Arrange
        mock_template = Mock(spec=Template)

        mock_template_filename = "Schema"
        mock_template_content = "<schema></schema>"
        mock_template_hash = ""
        mock_template_id = ObjectId()

        mock_template.filename = mock_template_filename
        mock_template.content = mock_template_content
        mock_template.hash = mock_template_hash
        mock_template.id = mock_template_id

        mock_save.return_value = mock_template

        # Act + Assert
        with self.assertRaises(exceptions.XSDError):
            template_api.create(mock_template_filename, mock_template_content)
