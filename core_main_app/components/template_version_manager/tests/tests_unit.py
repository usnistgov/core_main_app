from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch

from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager


class TestTemplateVersionManagerCreate(TestCase):

    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.create')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_returns_version_manager(self, mock_save_template, mock_create_version_manager):
        # Arrange
        mock_template_filename = "Schema"
        mock_template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        mock_template = _create_mock_template(mock_template_filename, mock_template_content)

        mock_save_template.return_value = mock_template

        mock_version_manager = Mock(spec=TemplateVersionManager)
        mock_create_version_manager.return_value = mock_version_manager

        # Act
        result = version_manager_api.create_manager("Schema", mock_template_filename, mock_template_content)

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_throws_exception_if_error_in_create_template(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            version_manager_api.create_manager("test", "test", "test")

    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.create')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_throws_exception_if_error_in_create_version_manager(self, mock_save_template,
                                                                                        mock_create_version_manager):
        # Arrange
        mock_template_filename = "Schema"
        mock_template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        mock_template = _create_mock_template(mock_template_filename, mock_template_content)

        mock_save_template.return_value = mock_template

        mock_create_version_manager.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            version_manager_api.create_manager("test", "test", "test")


class TestTemplateVersionManagerCreateVersion(TestCase):

    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.get_by_id')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_returns_template_version(self, mock_save_template, mock_get_by_id):
        # Arrange
        mock_template_filename = "Schema"
        mock_template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        mock_template = _create_mock_template(mock_template_filename, mock_template_content)
        mock_save_template.return_value = mock_template

        mock_version_manager = Mock(spec=TemplateVersionManager)
        mock_version_manager.id = ObjectId()
        mock_get_by_id.return_value = mock_version_manager

        # Act
        result = version_manager_api.create_version(mock_version_manager.id, mock_template_filename, mock_template_content)

        # Assert
        self.assertIsInstance(result, Template)

    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.get_by_id')
    def test_create_version_throws_exception_if_version_manager_id_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            version_manager_api.create_version("test", "test", "test")

    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.get_by_id')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_throws_exception_if_error_in_create_template(self, mock_save_template, mock_get_by_id):
        # Arrange
        mock_version_manager = Mock(spec=TemplateVersionManager)
        mock_version_manager.id = ObjectId()
        mock_get_by_id.return_value = mock_version_manager

        mock_save_template.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            version_manager_api.create_manager("test", "test", "test")


class TestTemplateVersionManagerGetGlobalVersions(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_global_versions')
    def test_get_global_versions_returns_templates(self, mock_get_global_versions):
        # Arrange
        mock_template1 = Mock(spec=Template)
        mock_template2 = Mock(spec=Template)

        mock_get_global_versions.return_value = [mock_template1, mock_template2]

        result = version_manager_api.get_global_versions()

        # Assert
        self.assertTrue(all(isinstance(item, Template) for item in result))


def _create_mock_template(mock_template_filename, mock_template_content):
    """
    Return a mock template
    :param mock_template_filename:
    :param mock_template_content:
    :return:
    """
    mock_template = Mock(spec=Template)
    mock_template.filename = mock_template_filename
    mock_template.content = mock_template_content
    mock_template.id = ObjectId()
    return mock_template
