from unittest.case import TestCase
from bson.objectid import ObjectId
from django.core import exceptions as django_exceptions
from mock.mock import Mock, patch
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager


class TestTemplateVersionManagerInitAndSave(TestCase):
    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.save')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_returns_version_manager(self, mock_save_template,
                                                            mock_save_template_version_manager):
        # Arrange
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.return_value = template

        version_manager = _create_template_version_manager(title="Schema")
        mock_save_template_version_manager.return_value = version_manager

        # Act
        result = version_manager_api.insert(version_manager, template)

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @patch('core_main_app.components.template.models.Template.delete')
    @patch('core_main_app.components.template.models.Template.save')
    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.save')
    def test_insert_manager_raises_api_error_if_title_already_exists(self, mock_version_manager_save,
                                                                     mock_template_save,
                                                                     mock_template_delete):
        # Arrange
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_template_save.return_value = template
        mock_template_delete.return_value = None
        mock_version_manager = _create_template_version_manager(title="Schema")
        mock_version_manager_save.side_effect = django_exceptions.ValidationError("")

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(mock_version_manager, template)

    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_raises_exception_if_error_in_create_template(self, mock_save):
        # Arrange
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_version_manager = _create_mock_template_version_manager(title="Schema")
        mock_save.side_effect = django_exceptions.ValidationError("")

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(mock_version_manager, template)

    @patch('core_main_app.components.template.models.Template.delete')
    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.save')
    @patch('core_main_app.components.template.models.Template.save')
    def test_create_version_manager_raises_exception_if_error_in_create_version_manager(self, mock_save_template,
                                                                                        mock_save_version_manager,
                                                                                        mock_delete_template):
        # Arrange
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.return_value = template
        version_manager = _create_template_version_manager(title="Schema")
        mock_save_version_manager.side_effect = django_exceptions.ValidationError("")
        mock_delete_template.return_value = None

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(version_manager, template)


class TestTemplateVersionManagerAddVersion(TestCase):
    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.insert')
    @patch('core_main_app.components.template.models.Template.save')
    @patch('core_main_app.components.template_version_manager.models.TemplateVersionManager.save')
    def test_insert_returns_template_version(self, mock_save_template_version_manager, mock_save_template, mock_insert):
        # Arrange
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        template = _create_template(template_filename, template_content)
        mock_save_template.return_value = template
        version_manager = _create_template_version_manager()
        mock_save_template_version_manager.return_value = version_manager
        mock_insert.return_value = version_manager
        # Act
        result = version_manager_api.insert(version_manager, template)

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @patch('core_main_app.components.template.models.Template.save')
    def test_insert_raises_exception_if_error_in_create_template(self, mock_save_template):
        # Arrange
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.side_effect = django_exceptions.ValidationError("")

        mock_version_manager = _create_mock_template_version_manager()

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(mock_version_manager, template)


class TestTemplateVersionManagerGetGlobalVersions(TestCase):

    @patch('core_main_app.components.version_manager.models.VersionManager.get_global_version_managers')
    def test_get_global_version_managers_returns_templates(self, mock_get_global_version_managers):
        # Arrange
        mock_template1 = _create_mock_template()
        mock_template2 = _create_mock_template()

        mock_get_global_version_managers.return_value = [mock_template1, mock_template2]

        result = version_manager_api.get_global_version_managers()

        # Assert
        self.assertTrue(all(isinstance(item, Template) for item in result))


def _create_mock_template(mock_template_filename="", mock_template_content=""):
    """
    Returns a mock template
    :param mock_template_filename:
    :param mock_template_content:
    :return:
    """
    mock_template = Mock(spec=Template)
    mock_template.filename = mock_template_filename
    mock_template.content = mock_template_content
    mock_template.id = ObjectId()
    return mock_template


def _create_mock_template_version_manager(title=""):
    """
    Returns a mock template version manager
    :return:
    """
    mock_template_version_manager = Mock(spec=TemplateVersionManager)
    mock_template_version_manager.title = title
    mock_template_version_manager.id = ObjectId()
    mock_template_version_manager.versions = []
    mock_template_version_manager.disabled_versions = []
    return mock_template_version_manager


def _create_template(filename="", content=""):
    """
    Returns a template
    :param filename:
    :param content:
    :return:
    """
    return Template(
        id=ObjectId(),
        filename=filename,
        content=content
    )


def _create_template_version_manager(title=""):
    """
    Returns a templates version manager
    :param title:
    :return:
    """
    return TemplateVersionManager(
        id=ObjectId(),
        title=title,
        versions=[],
        disabled_versions=[]
    )
