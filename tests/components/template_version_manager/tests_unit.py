""" Template Version Manager unit tests
"""
from unittest.case import TestCase

from bson.objectid import ObjectId
from django.core import exceptions as django_exceptions
from django.test import override_settings
from mock.mock import Mock, patch, MagicMock
from mongoengine import errors as mongoengine_errors

from core_main_app.commons.exceptions import NotUniqueError, ModelError
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as version_manager_api
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestTemplateVersionManagerInsert(TestCase):
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_returns_version_manager(
        self, mock_save_template, mock_save_template_version_manager
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.return_value = template

        version_manager = _create_template_version_manager(title="Schema")
        mock_save_template_version_manager.return_value = version_manager

        # Act
        result = version_manager_api.insert(
            version_manager, template, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.delete")
    @patch("core_main_app.components.template.models.Template.save")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    def test_insert_manager_raises_api_error_if_title_already_exists(
        self, mock_version_manager_save, mock_template_save, mock_template_delete
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_template_save.return_value = template
        mock_template_delete.return_value = None
        mock_version_manager = _create_template_version_manager(title="Schema")
        mock_version_manager_save.side_effect = mongoengine_errors.NotUniqueError("")

        # Act + Assert
        with self.assertRaises(NotUniqueError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_raises_exception_if_error_in_create_template(
        self, mock_save
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_version_manager = _create_mock_template_version_manager(title="Schema")
        mock_save.side_effect = django_exceptions.ValidationError("")

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.delete")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_raises_exception_if_error_in_create_version_manager(
        self, mock_save_template, mock_save_version_manager, mock_delete_template
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.return_value = template
        version_manager = _create_template_version_manager(title="Schema")
        mock_save_version_manager.side_effect = django_exceptions.ValidationError("")
        mock_delete_template.return_value = None

        # Act + Assert
        with self.assertRaises(ModelError):
            version_manager_api.insert(version_manager, template, request=mock_request)


class TestTemplateVersionManagerAddVersion(TestCase):
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.insert"
    )
    @patch("core_main_app.components.template.models.Template.save")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    def test_insert_returns_template_version(
        self, mock_save_template_version_manager, mock_save_template, mock_insert
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        template = _create_template(template_filename, template_content)
        mock_save_template.return_value = template
        version_manager = _create_template_version_manager()
        mock_save_template_version_manager.return_value = version_manager
        mock_insert.return_value = version_manager
        # Act
        result = version_manager_api.insert(
            version_manager, template, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save")
    def test_insert_raises_exception_if_error_in_create_template(
        self, mock_save_template
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.side_effect = django_exceptions.ValidationError("")

        mock_version_manager = _create_mock_template_version_manager()

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )


class TestTemplateVersionManagerGetGlobalVersions(TestCase):
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager."
        "get_global_version_managers"
    )
    def test_get_global_version_managers_returns_templates(
        self, mock_get_global_version_managers
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        mock_template1 = _create_mock_template()
        mock_template2 = _create_mock_template()

        mock_get_global_version_managers.return_value = [mock_template1, mock_template2]

        result = version_manager_api.get_global_version_managers(request=mock_request)

        # Assert
        self.assertTrue(all(isinstance(item, Template) for item in result))


class TestTemplateVersionManagerGetActiveGlobalVersions(TestCase):
    @patch(
        "core_main_app.components.version_manager.models.VersionManager.get_active_global_version_manager"
    )
    def test_get_active_global_version_managers_returns_templates_not_disable(
        self, mock_get_active_global_version_managers
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        mock_template1 = _create_template_version_manager("test1")
        mock_template2 = _create_template_version_manager("test2")

        queryset = MagicMock()
        queryset.filter.return_value = queryset
        queryset.all.return_value = [mock_template1, mock_template2]
        mock_get_active_global_version_managers.return_value = queryset

        result = version_manager_api.get_active_global_version_manager(
            request=mock_request
        )

        # Assert
        self.assertTrue(all(item.is_disabled is False for item in result))


class TestTemplateVersionManagerGetActiveGlobalVersionsByUserId(TestCase):
    @patch(
        "core_main_app.components.version_manager.models.VersionManager.get_active_version_manager_by_user_id"
    )
    def test_get_active_global_version_managers_by_user_id_returns_templates_not_disable_with_given_user_id(
        self, mock_get_active_global_version_managers
    ):
        # Arrange
        user_id = "10"
        mock_user = create_mock_user(user_id, is_superuser=True)
        mock_request = create_mock_request(mock_user)
        mock_template1 = _create_template_version_manager(user_id=user_id)
        mock_template2 = _create_template_version_manager(user_id=user_id)

        queryset = MagicMock()
        queryset.filter.return_value = queryset
        queryset.all.return_value = [mock_template1, mock_template2]
        mock_get_active_global_version_managers.return_value = queryset

        result = version_manager_api.get_active_version_manager_by_user_id(
            request=mock_request
        )

        # Assert
        self.assertTrue(
            all(
                item.is_disabled is False and item.user == str(user_id)
                for item in result
            )
        )


class TestTemplateVersionManagerGetAllByVersionIds(TestCase):
    @patch.object(TemplateVersionManager, "get_all_by_version_ids")
    def test_get_all_by_version_ids(self, mock_get_all_by_version_ids):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        version_x = ObjectId()
        version_y = ObjectId()
        mock_template1 = _create_mock_template_version_manager("mock1", [version_x])
        mock_template2 = _create_mock_template_version_manager("mock2", [version_y])

        mock_get_all_by_version_ids.return_value = [mock_template1, mock_template2]

        result = version_manager_api.get_all_by_version_ids(
            [version_x, version_y], request=mock_request
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, TemplateVersionManager) for item in result)
        )


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


def _create_mock_template_version_manager(
    title="", versions=None, is_disabled=False, user_id=""
):
    """
    Returns a mock template version manager
    :return:
    """
    if versions is None:
        versions = []
    mock_template_version_manager = Mock(spec=TemplateVersionManager)
    mock_template_version_manager.title = title
    mock_template_version_manager.id = ObjectId()
    mock_template_version_manager.versions = versions
    mock_template_version_manager.disabled_versions = []
    mock_template_version_manager.is_disabled = is_disabled
    mock_template_version_manager.user = str(user_id)
    mock_template_version_manager._cls = TemplateVersionManager.class_name
    return mock_template_version_manager


def _create_template(filename="", content=""):
    """
    Returns a template
    :param filename:
    :param content:
    :return:
    """
    return Template(id=ObjectId(), filename=filename, content=content)


def _create_template_version_manager(title="", is_disabled=False, user_id=""):
    """
    Returns a templates version manager
    :param title:
    :return:
    """
    return TemplateVersionManager(
        id=ObjectId(),
        title=title,
        versions=[],
        user=user_id,
        is_disabled=is_disabled,
        disabled_versions=[],
        _cls=TemplateVersionManager.class_name,
    )
