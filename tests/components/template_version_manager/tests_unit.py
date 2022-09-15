""" Template Version Manager unit tests
"""
from unittest.case import TestCase

from django.core import exceptions as django_exceptions
from django.core.exceptions import ValidationError
from django.test import override_settings
from mock.mock import Mock, patch, MagicMock

from core_main_app.commons.exceptions import DoesNotExist, NotUniqueError
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import api as version_manager_api
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestTemplateVersionManagerGet(TestCase):
    """TestTemplateVersionManagerGet"""

    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.get_by_id"
    )
    def test_version_manager_get_returns_version_manager(self, mock_get_by_id):
        """test version manager get returns version manager

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        mock_version_manager = _create_template_version_manager(title="Schema")

        mock_get_by_id.return_value = mock_version_manager

        # Act
        result = version_manager_api.get_by_id(
            mock_version_manager.id, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.get_by_id"
    )
    def test_version_manager_get_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test version manager get raises exception if object does not exist

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        mock_absent_id = -1
        mock_get_by_id.side_effect = DoesNotExist("")

        # Act + Assert
        with self.assertRaises(DoesNotExist):
            version_manager_api.get_by_id(mock_absent_id, request=mock_request)


class TestTemplateVersionManagerInsert(TestCase):
    """TestTemplateVersionManagerInsert"""

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch.object(TemplateVersionManager, "save_version_manager")
    @patch("core_main_app.components.template.models.Template.save_template")
    def test_create_version_manager_returns_version_manager(
        self, mock_save_template, mock_save_template_version_manager
    ):
        """test create version manager returns version manager

        Args:
            mock_save_template:
            mock_save_template_version_manager:

        Returns:

        """
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
    @patch("core_main_app.components.template.models.Template.save_template")
    @patch.object(TemplateVersionManager, "save_version_manager")
    def test_insert_manager_raises_api_error_if_title_already_exists(
        self, mock_version_manager_save, mock_template_save, mock_template_delete
    ):
        """test insert manager raises api error if title already exists

        Args:
            mock_version_manager_save:
            mock_template_save:
            mock_template_delete:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_template_save.return_value = template
        mock_template_delete.return_value = None
        mock_version_manager = _create_template_version_manager(title="Schema")
        mock_version_manager_save.side_effect = NotUniqueError("")

        # Act + Assert
        with self.assertRaises(NotUniqueError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save_template")
    def test_create_version_manager_raises_exception_if_error_in_create_template(
        self, mock_save
    ):
        """test create version manager raises exception if error in create template

        Args:
            mock_save:

        Returns:

        """
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
    @patch.object(TemplateVersionManager, "save_version_manager")
    @patch("core_main_app.components.template.models.Template.save_template")
    def test_create_version_manager_raises_exception_if_error_in_create_version_manager(
        self, mock_save_template, mock_save_version_manager, mock_delete_template
    ):
        """test create version manager raises exception if error in create version manager

        Args:
            mock_save_template:
            mock_save_version_manager:
            mock_delete_template:

        Returns:

        """
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
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(version_manager, template, request=mock_request)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.delete")
    @patch.object(TemplateVersionManager, "save_version_manager")
    @patch("core_main_app.components.template.models.Template.save_template")
    def test_create_version_manager_raises_exception_if_title_is_empty(
        self, mock_save_template, mock_save_version_manager, mock_delete_template
    ):
        """test create version manager raises exception if title is empty

        Args:
            mock_save_template:
            mock_save_version_manager:
            mock_delete_template:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.return_value = template
        version_manager = _create_template_version_manager(title="")
        mock_save_version_manager.side_effect = django_exceptions.ValidationError("")
        mock_delete_template.return_value = None

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(version_manager, template, request=mock_request)


class TestTemplateVersionManagerAddVersion(TestCase):
    """TestTemplateVersionManagerAddVersion"""

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    def test_insert_returns_template_version(
        self, mock_save_template_version_manager, mock_save_template
    ):
        """test insert returns template version

        Args:
            mock_save_template_version_manager:
            mock_save_template:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "Schema"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"

        template = _create_template(template_filename, template_content)
        mock_save_template.return_value = template
        version_manager = _create_template_version_manager()
        mock_save_template_version_manager.return_value = version_manager
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
        """test insert raises exception if error in create template

        Args:
            mock_save_template:

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template_filename = "schema.xsd"
        template_content = "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        template = _create_template(template_filename, template_content)

        mock_save_template.side_effect = django_exceptions.ValidationError("")

        mock_version_manager = _create_mock_template_version_manager()

        # Act + Assert
        with self.assertRaises(ValidationError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )


class TestTemplateVersionManagerGetGlobalVersions(TestCase):
    """TestTemplateVersionManagerGetGlobalVersions"""

    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager."
        "get_global_version_managers"
    )
    def test_get_global_version_managers_returns_templates(
        self, mock_get_global_version_managers
    ):
        """test get global version managers returns templates

        Args:
            mock_get_global_version_managers:

        Returns:

        """
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
    """TestTemplateVersionManagerGetActiveGlobalVersions"""

    @patch.object(TemplateVersionManager, "get_active_global_version_manager")
    def test_get_active_global_version_managers_returns_templates_not_disable(
        self, mock_get_active_global_version_managers
    ):
        """test get active global version managers returns templates not disable

        Args:
            mock_get_active_global_version_managers:

        Returns:

        """
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
    """TestTemplateVersionManagerGetActiveGlobalVersionsByUserId"""

    @patch.object(TemplateVersionManager, "get_active_version_manager_by_user_id")
    def test_get_active_global_version_managers_by_user_id_returns_templates_not_disable_with_given_user_id(
        self, mock_get_active_global_version_managers
    ):
        """test get active global version managers by user id
        returns templates not disable with given user id

        Args:
            mock_get_active_global_version_managers:

        Returns:

        """
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


def _create_mock_template(mock_template_filename="", mock_template_content=""):
    """create mock template

    Args:
        mock_template_filename:
        mock_template_content:

    Returns:

    """
    mock_template = Mock(spec=Template)
    mock_template.filename = mock_template_filename
    mock_template.content = mock_template_content
    mock_template.id = 1
    return mock_template


def _create_mock_template_version_manager(
    title="", versions=None, is_disabled=False, user_id=""
):
    """create mock template version manager

    Args:
        title:
        versions:
        is_disabled:
        user_id:

    Returns:

    """
    if versions is None:
        versions = []
    mock_template_version_manager = Mock(spec=TemplateVersionManager)
    mock_template_version_manager.title = title
    mock_template_version_manager.id = 1
    mock_template_version_manager.versions = versions
    mock_template_version_manager.disabled_versions = []
    mock_template_version_manager.is_disabled = is_disabled
    mock_template_version_manager.user = str(user_id)
    mock_template_version_manager._cls = TemplateVersionManager.class_name
    return mock_template_version_manager


def _create_template(filename="", content=""):
    """create template

    Args:
        filename:
        content:

    Returns:

    """
    return Template(id=1, filename=filename, content=content)


def _create_template_version_manager(title="Schema", is_disabled=False, user_id=""):
    """create template version manager

    Args:
        title:
        is_disabled:
        user_id:

    Returns:

    """
    return TemplateVersionManager(
        id=1,
        title=title,
        user=user_id,
        is_disabled=is_disabled,
        _cls=TemplateVersionManager.class_name,
    )
