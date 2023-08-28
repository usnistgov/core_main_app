""" Test units
"""
from unittest.case import TestCase
from unittest.mock import Mock, patch, MagicMock

from django.test import override_settings

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist, CoreError
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestTemplateGet(TestCase):
    """TestTemplateGet"""

    @patch("core_main_app.components.template.models.Template.get_by_id")
    def test_template_get_returns_template(self, mock_get_by_id):
        """test template get returns template

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_template_filename = "Schema"
        mock_template_content = (
            "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
        )

        mock_template = _create_mock_template(
            mock_template_filename, mock_template_content
        )

        mock_get_by_id.return_value = mock_template
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = template_api.get_by_id(mock_template.id, request=mock_request)

        # Assert
        self.assertIsInstance(result, Template)

    @patch("core_main_app.components.template.models.Template.get_by_id")
    def test_template_get_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test template get raises exception if object does not exist

        Args:
            mock_get_by_id:

        Returns:

        """
        # Arrange
        mock_absent_id = -1
        mock_get_by_id.side_effect = DoesNotExist("")
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)

        # Act + Assert
        with self.assertRaises(DoesNotExist):
            template_api.get_by_id(mock_absent_id, request=mock_request)


class TestTemplateGetAllByHash(TestCase):
    """TestTemplateGetAllByHash"""

    @patch("core_main_app.components.template.models.Template.get_all_by_hash")
    def test_template_get_all_by_hash_contains_only_template(
        self, mock_get_all_by_hash
    ):
        """test template get all by hash contains only template

        Args:
            mock_get_all_by_hash:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        _generic_get_all_test(
            self,
            mock_get_all_by_hash,
            template_api.get_all_accessible_by_hash(
                "fake_hash", request=mock_request
            ),
        )


class TestTemplateUpsert(TestCase):
    """TestTemplateUpsert"""

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save")
    def test_template_upsert_valid_returns_template(self, mock_save):
        """test template upsert valid returns template

        Args:
            mock_save:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = _create_template(
            filename="name.xsd",
            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
        )

        mock_save.return_value = template
        result = template_api.upsert(template, request=mock_request)
        self.assertIsInstance(result, Template)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    @patch("core_main_app.components.template.models.Template.save")
    def test_template_upsert_invalid_filename_raises_core_error(
        self, mock_save
    ):
        """test template upsert invalid filename raises core error

        Args:
            mock_save:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = _create_template(
            filename="1",
            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
        )

        with self.assertRaises(CoreError):
            template_api.upsert(template, request=mock_request)

    @patch("core_main_app.components.template.models.Template.save")
    def test_template_upsert_invalid_content_raises_xsd_error(self, mock_save):
        """test template upsert invalid content raises xsd error

        Args:
            mock_save:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = _create_template(
            filename="name.xsd", content="<schema></schema>"
        )
        mock_save.return_value = None
        with self.assertRaises(exceptions.XSDError):
            template_api.upsert(template, request=mock_request)

    @patch("core_main_app.components.template.models.Template.save")
    def test_template_upsert_no_content_raises_error(self, mock_save):
        """test template upsert no content raises error

        Args:
            mock_save:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = _create_template(filename="name.xsd")
        mock_save.return_value = None
        with self.assertRaises(Exception):
            template_api.upsert(template, request=mock_request)

    @patch("core_main_app.utils.json_utils.is_schema_valid")
    @patch(
        "core_main_app.components.template.api._register_local_dependencies"
    )
    @patch("core_main_app.utils.xml.get_hash")
    @patch("core_main_app.utils.xml.is_schema_valid")
    @patch("core_main_app.components.template.models.Template.save")
    def test_xsd_template_upsert_calls_xml_functions(
        self,
        mock_save,
        mock_is_xml_schema_valid,
        mock_get_hash,
        mock_register_local_dependencies,
        mock_is_json_schema_valid,
    ):
        """test_xsd_template_upsert_calls_xml_functions

        Args:
            mock_save:
            mock_is_xml_schema_valid:
            mock_get_hash:
            mock_register_local_dependencies:
            mock_is_json_schema_valid:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = MagicMock()
        template.filename = "file.xsd"
        mock_save.return_value = None
        template_api.upsert(template, request=mock_request)
        self.assertTrue(mock_is_xml_schema_valid.called)
        self.assertTrue(mock_get_hash.called)
        self.assertTrue(mock_register_local_dependencies.called)
        self.assertFalse(mock_is_json_schema_valid.called)

    @patch("core_main_app.utils.json_utils.is_schema_valid")
    @patch(
        "core_main_app.components.template.api._register_local_dependencies"
    )
    @patch("core_main_app.utils.xml.get_hash")
    @patch("core_main_app.utils.xml.is_schema_valid")
    @patch("core_main_app.components.template.models.Template.save")
    def test_json_template_upsert_calls_json_functions(
        self,
        mock_save,
        mock_is_xml_schema_valid,
        mock_get_hash,
        mock_register_local_dependencies,
        mock_is_json_schema_valid,
    ):
        """test_json_template_upsert_calls_json_functions

        Args:
            mock_save:
            mock_is_xml_schema_valid:
            mock_get_hash:
            mock_register_local_dependencies:
            mock_is_json_schema_valid:

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(mock_user)
        template = MagicMock()
        template.filename = "file.json"
        mock_save.return_value = None
        template_api.upsert(template, request=mock_request)
        self.assertFalse(mock_is_xml_schema_valid.called)
        self.assertFalse(mock_get_hash.called)
        self.assertFalse(mock_register_local_dependencies.called)
        self.assertTrue(mock_is_json_schema_valid.called)


class TestTemplateHash(TestCase):
    """TestTemplateHash"""

    def test_template_hash_returns_hash_if_set(self):
        """test_template_hash_returns_hash_if_set

        Args:

        Returns:

        """
        template = _create_template(
            filename="name.xsd",
            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
        )
        template._hash = "hash"

        self.assertEqual(template.hash, "hash")

    def test_template_hash_returns_checksum_if_hash_not_set(self):
        """test_template_hash_returns_checksum_if_hash_not_set

        Args:

        Returns:

        """
        template = _create_template(
            filename="name.xsd",
            content="<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>",
        )
        template._hash = None
        template.checksum = "checksum"

        self.assertEqual(template.hash, "checksum")


def _generic_get_all_test(self, mock_get_all, act_function):
    """generic get all test

    Args:
        self:
        mock_get_all:
        act_function:

    Returns:

    """
    # Arrange
    mock_template_filename = "Schema"
    mock_template_content = (
        "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
    )

    mock_template_1 = _create_mock_template(
        mock_template_filename, mock_template_content
    )
    mock_template_2 = _create_mock_template(
        mock_template_filename, mock_template_content
    )
    mock_get_all.return_value = [mock_template_1, mock_template_2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, Template) for item in result))


def _create_template(filename="", content=""):
    """create template

    Args:
        filename:
        content:

    Returns:

    """
    return Template(id=1, filename=filename, content=content)


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
