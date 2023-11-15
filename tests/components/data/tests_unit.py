""" Unit Test Data
"""
import json
from collections import OrderedDict
from json import JSONDecodeError
from time import sleep
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import CoreError
from core_main_app.components.abstract_data.models import AbstractData
from core_main_app.components.blob.models import Blob
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.datetime import datetime_now, datetime_timedelta
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestDataGetById(TestCase):
    """TestDataGetById"""

    @patch.object(Data, "get_by_id")
    def test_data_get_by_id_raises_api_error_if_not_found(self, mock_get):
        """test_data_get_by_id_raises_api_error_if_not_found

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_user = create_mock_user("1")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_api.get_by_id(1, mock_user)

    @patch.object(Data, "get_by_id")
    def test_data_get_by_id_return_data_if_found(self, mock_get):
        """test_data_get_by_id_return_data_if_found

        Args:
            mock_get:

        Returns:

        """
        # Arrange
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get.return_value = mock_data
        mock_user = create_mock_user("1")
        # Act
        result = data_api.get_by_id(1, mock_user)
        # Assert
        self.assertIsInstance(result, Data)


class TestDataUpsert(TestCase):
    """TestDataUpsert"""

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_return_data_with_new_title_if_is_called_with_only_title_modified(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_return_data_with_new_title_if_is_called_with_only_title_modified

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(),
            user_id="2",
            title="new_title",
            content="<tag></tag>",
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("2")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertEqual("new_title", result.title)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_return_data_with_new_user_id_if_is_called_with_only_user_id_modified(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_return_data_with_new_user_id_if_is_called_with_only_user_id_modified

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(),
            user_id="3",
            title="new_title",
            content="<tag></tag>",
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertEqual("3", result.user_id)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_return_data_with_new_xml_if_is_called_with_only_xml_modified(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_return_data_with_new_xml_if_is_called_with_only_xml_modified

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        xml = "<new_tag></new_tag>"
        data = _create_data(
            _get_template(), user_id="3", title="title", content=xml
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertEqual(xml, result.xml_content)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_return_data_with_last_modification_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_return_data_with_last_modification_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(result.last_modification_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_updates_last_modification_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_updates_last_modification_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        creation_date = result.last_modification_date
        sleep(0.05)
        # Assert
        data_api.upsert(data, mock_request)
        self.assertNotEqual(creation_date, data.last_modification_date)

    def test_data_upsert_raises_xml_error_if_failed_during_xml_validation(
        self,
    ):
        """test_data_upsert_raises_xml_error_if_failed_during_xml_validation

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content=""
        )
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.upsert(data, mock_request)

    def test_data_upsert_raises_xsd_error_if_failed_during_xsd_validation(
        self,
    ):
        """test_data_upsert_raises_xsd_error_if_failed_during_xsd_validation

        Returns:

        """
        # Arrange
        template = _get_template()
        template.content += "<"
        data = _create_data(
            template, user_id="3", title="title", content="<new_tag></new_tag>"
        )
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(exceptions.XSDError):
            data_api.upsert(data, mock_request)

    def test_data_upsert_raises_xml_error_if_failed_during_validation(self):
        """test_data_upsert_raises_xml_error_if_failed_during_validation

        Returns:

        """
        # Arrange
        template = _get_template()
        data = _create_data(
            template, user_id="3", title="title", content="<new_tag></new_tag>"
        )
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.upsert(data, mock_request)

    def test_data_upsert_without_xml_content_raises_api_error(self):
        """test_data_without_xml_content_upsert_raises_api_error

        Returns:

        """
        # Arrange
        template = _get_template()
        data = _create_data(template, user_id="1", title="title", content=None)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.upsert(data, mock_request)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    def test_xml_data_upsert_calls_xml_validation(
        self, mock_check_xml_file_is_valid, mock_check_json_file_is_valid
    ):
        """test_xml_data_upsert_calls_xml_validation

        Returns:

        """
        # Arrange
        template = MagicMock()
        template.format = Template.XSD
        data = MagicMock()
        data.template = template
        mock_user = create_mock_user(1, is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        # Assert
        self.assertTrue(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    def test_json_data_upsert_calls_json_validation(
        self, mock_check_xml_file_is_valid, mock_check_json_file_is_valid
    ):
        """test_json_data_upsert_calls_json_validation

        Returns:

        """
        # Arrange
        template = MagicMock()
        template.format = Template.JSON
        data = MagicMock()
        data.template = template
        mock_user = create_mock_user(1, is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertTrue(mock_check_json_file_is_valid.called)

    @patch.object(Data, "save")
    def test_data_upsert_json_format_returns_data_with_dict_content_set(
        self, mock_save
    ):
        """test_data_upsert_json_format_returns_data_with_dict_content_set

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content=json.dumps({"element": "value"}),
        )
        mock_save.return_value = data
        mock_user = create_mock_user("2")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertIsInstance(result.content, str)
        self.assertIsInstance(result.dict_content, dict)

    @patch("core_main_app.components.data.models.Data.convert_to_file")
    def test_data_upsert_unknown_format_convert_to_file_raises_model_error(
        self, mock_convert_to_file
    ):
        """test_data_upsert_unknown_format_convert_to_file_raises_model_error

        Args:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content={"element": "value"},
        )
        data.template.format = "bad"
        mock_user = create_mock_user("2")
        mock_request = create_mock_request(user=mock_user)
        # Act + Assert
        with self.assertRaises(CoreError):
            data_api.upsert(data, mock_request)

    @patch("core_main_app.components.data.models.Data.convert_to_dict")
    def test_data_upsert_unknown_format_convert_to_dict_raises_model_error(
        self, mock_convert_to_dict
    ):
        """test_data_upsert_unknown_format_convert_to_dict_raises_model_error

        Args:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content={"element": "value"},
        )
        data.template.format = "bad"
        mock_user = create_mock_user("2")
        mock_request = create_mock_request(user=mock_user)
        # Act + Assert
        with self.assertRaises(CoreError):
            data_api.upsert(data, mock_request)

    @patch("django.core.files.uploadedfile.SimpleUploadedFile.__init__")
    @patch("core_main_app.utils.xml.raw_xml_to_dict")
    @patch.object(Data, "content")
    @patch.object(Data, "save")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    def test_data_encoding_error_returns_data_with_content_set(
        self,
        mock_check_xml,
        mock_data_save,
        mock_data_content,
        mock_raw_xml_to_dict,
        mock_simple_upload_file,
    ):
        """test_data_encoding_error_returns_data_with_content_set

        Args:

        Returns:

        """
        # Arrange
        mock_simple_upload_file.return_value = None
        mock_content = MagicMock()
        mock_content.encode.side_effect = UnicodeEncodeError("", "", 0, 0, "")
        mock_data_content.return_value = mock_content
        data = _create_data(
            _get_template(),
            user_id="2",
            title="title",
            content=mock_content,
        )
        # mock_check_xml.return_value = None

        mock_user = create_mock_user("2")
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.upsert(data, mock_request)
        # Assert
        self.assertTrue(result.content, data.content)


class TestAdminDataInsert(TestCase):
    """TestAdminDataInsert"""

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_custom_last_modification_date_if_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_custom_last_modification_date_if_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        yesterday = datetime_now() - datetime_timedelta(days=1)
        data.last_modification_date = yesterday
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertEqual(result.last_modification_date, yesterday)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_last_modification_date_if_not_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_last_modification_date_if_not_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertIsNotNone(result.last_modification_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_custom_creation_date_if_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_custom_creation_date_if_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        yesterday = datetime_now() - datetime_timedelta(days=1)
        data.creation_date = yesterday
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertEqual(result.creation_date, yesterday)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_creation_date_if_not_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_creation_date_if_not_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertIsNotNone(result.creation_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_custom_last_change_date_if_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_custom_last_change_date_if_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        yesterday = datetime_now() - datetime_timedelta(days=1)
        data.last_change_date = yesterday
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertEqual(result.last_change_date, yesterday)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_admin_insert_sets_last_change_date_if_not_provided(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_admin_insert_sets_last_change_date_if_not_provided

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertIsNotNone(result.last_change_date)

    def test_data_admin_insert_without_xml_content_raises_api_error(self):
        """test_data_admin_insert_without_xml_content_raises_api_error

        Returns:

        """
        # Arrange
        template = _get_template()
        data = _create_data(template, user_id="1", title="title", content=None)
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.admin_insert(data, request=mock_request)

    @patch.object(Data, "save")
    def test_admin_insert_json_format_returns_data_with_dict_content_set(
        self, mock_save
    ):
        """test_admin_insert_json_format_returns_data_with_dict_content_set

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content=json.dumps({"element": "value"}),
        )
        mock_save.return_value = data
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act
        result = data_api.admin_insert(data, request=mock_request)
        # Assert
        self.assertIsInstance(result.content, str)
        self.assertIsInstance(result.dict_content, dict)

    @patch("core_main_app.components.data.models.Data.convert_to_file")
    def test_admin_insert_unknown_format_convert_to_file_raises_model_error(
        self, mock_convert_to_file
    ):
        """test_admin_insert_unknown_format_convert_to_file_raises_model_error

        Args:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content={"element": "value"},
        )
        data.template.format = "bad"
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act + Assert
        with self.assertRaises(CoreError):
            data_api.admin_insert(data, request=mock_request)

    @patch("core_main_app.components.data.models.Data.convert_to_dict")
    def test_admin_insert_unknown_format_convert_to_dict_raises_model_error(
        self, mock_convert_to_dict
    ):
        """test_admin_insert_unknown_format_convert_to_dict_raises_model_error

        Args:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_json_template(),
            user_id="2",
            title="title",
            content={"element": "value"},
        )
        data.template.format = "bad"
        mock_user = create_mock_user("3", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        # Act + Assert
        with self.assertRaises(CoreError):
            data_api.admin_insert(data, request=mock_request)


class TestDataCheckXmlFileIsValid(TestCase):
    """TestDataCheckXmlFileIsValid"""

    def test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_xml_validation(
        self,
    ):
        """test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_xml_validation

        Returns:

        """
        # Arrange
        user = create_mock_user("3")
        mock_request = create_mock_request(user=user)
        data = _create_data(
            _get_template(), user_id="3", title="title", content=""
        )
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.check_xml_file_is_valid(data, request=mock_request)

    def test_data_check_xml_file_is_valid_raises_xsd_error_if_failed_during_xsd_validation(
        self,
    ):
        """test_data_check_xml_file_is_valid_raises_xsd_error_if_failed_during_xsd_validation

        Returns:

        """
        # Arrange
        user = create_mock_user("3")
        mock_request = create_mock_request(user=user)
        template = _get_template()
        template.content += "<"
        data = _create_data(
            template, user_id="3", title="title", content="<new_tag></new_tag>"
        )
        # Act # Assert
        with self.assertRaises(exceptions.XSDError):
            data_api.check_xml_file_is_valid(data, request=mock_request)

    def test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_validation(
        self,
    ):
        """test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_validation

        Returns:

        """
        # Arrange
        user = create_mock_user("3")
        mock_request = create_mock_request(user=user)
        template = _get_template()
        data = _create_data(
            template, user_id="3", title="title", content="<new_tag></new_tag>"
        )
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.check_xml_file_is_valid(data, request=mock_request)

    def test_data_check_xml_data_valid_return_true_if_validation_success(self):
        """test_data_check_xml_data_valid_return_true_if_validation_success

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        template = _get_template()
        data = _create_data(
            template, user_id="3", title="title", content="<tag>toto</tag>"
        )
        # Act
        result = data_api.check_xml_file_is_valid(data, request=mock_request)
        # Assert
        self.assertEqual(result, True)


class TestDataCheckJsonFileIsValid(TestCase):
    """TestDataCheckJsonFileIsValid"""

    def test_data_check_json_file_is_valid_raises_json_decode_error_if_invalid_format(
        self,
    ):
        """test_data_check_json_file_is_valid_raises_core_error_if_invalid_format

        Returns:

        """
        # Arrange
        template = MagicMock()
        template.content = {}
        data = MagicMock()
        data.template = template
        data.content = "test"
        # Act # Assert
        with self.assertRaises(JSONDecodeError):
            data_api.check_json_file_is_valid(data)

    def test_data_check_json_file_is_valid_raises_json_error_if_failed_during_json_validation(
        self,
    ):
        """test_data_check_json_file_is_valid_raises_json_error_if_failed_during_json_validation

        Returns:

        """
        # Arrange
        template = MagicMock()
        template.content = {
            "definitions": {},
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/root.json",
            "type": "object",
            "required": [
                "checked",
            ],
            "properties": {
                "checked": {
                    "$id": "#/properties/checked",
                    "type": "boolean",
                }
            },
        }
        data = MagicMock()
        data.template = template
        data.content = json.dumps({"checked": "bad value"})
        # Act # Assert
        with self.assertRaises(exceptions.JSONError):
            data_api.check_json_file_is_valid(data)

    def test_data_json_xml_data_valid_return_true_if_validation_successful(
        self,
    ):
        """test_data_json_xml_data_valid_return_true_if_validation_successful

        Returns:

        """
        # Arrange
        template = MagicMock()
        template.content = {}
        data = MagicMock()
        data.template = template
        data.content = json.dumps({"value": 1})
        # Act
        result = data_api.check_json_file_is_valid(data)
        # Assert
        self.assertEqual(result, True)


class TestDataGetNone(TestCase):
    """TestDataGetNone"""

    def test_data_get_none_returns_empty_list(
        self,
    ):
        """test_data_get_none_returns_empty_list

        Returns:

        """

        # Act
        result = data_api.get_none()
        # Assert
        self.assertEqual(len(result), 0)


class TestTimes(TestCase):
    """TestTimes"""

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_init_last_modification_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_init_last_modification_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.last_modification_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_init_last_change_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_init_last_change_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.last_change_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_upsert_init_creation_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_upsert_init_creation_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.creation_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_edit_content_updates_last_modification_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_edit_content_updates_last_modification_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        data.id = 1
        original_date = data.last_modification_date
        sleep(0.05)
        data.content = "<root></root>"
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.last_modification_date)
        self.assertTrue(data.last_modification_date > original_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_edit_metadata_does_not_update_last_modification_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_edit_metadata_does_not_update_last_modification_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        data.id = 1
        original_date = data.last_modification_date
        data.title = "test"
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.last_modification_date)
        self.assertEqual(data.last_modification_date, original_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_edit_metadata_updates_last_change_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_edit_metadata_updates_last_change_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        data.id = 1
        original_date = data.last_change_date
        data.title = "test"
        sleep(0.05)
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.last_change_date)
        self.assertTrue(data.last_change_date > original_date)

    @patch.object(Data, "convert_to_file")
    @patch.object(data_api, "check_xml_file_is_valid")
    @patch.object(Data, "save")
    def test_data_edit_does_not_updates_creation_date(
        self, mock_save, mock_check, mock_convert_file
    ):
        """test_data_edit_does_not_updates_creation_date

        Args:
            mock_save:
            mock_check:
            mock_convert_file:

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="3", title="title", content="<tag></tag>"
        )
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act
        data_api.upsert(data, mock_request)
        data.id = 1
        original_date = data.creation_date
        data.title = "test"
        data_api.upsert(data, mock_request)
        # Assert
        self.assertIsNotNone(data.creation_date)
        self.assertEqual(data.creation_date, original_date)


class TestDataBlob(TestCase):
    """TestDataBlob"""

    def test_data_blob_none_return_none(
        self,
    ):
        """test_data_blob_none_return_none

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(),
            user_id="2",
            title="new_title",
            content="<tag></tag>",
        )
        user = create_mock_user("2")
        # Act
        blob = data.blob(user=user)
        # Assert
        self.assertIsNone(blob)

    def test_data_blob_return_blob(
        self,
    ):
        """test_data_blob_return_blob

        Returns:

        """
        # Arrange
        data = _create_data(
            template=_get_template(),
            user_id="2",
            title="new_title",
            content="<tag></tag>",
            blob=_create_blob(user_id="2"),
        )
        user = create_mock_user("2")
        # Act
        blob = data.blob(user=user)
        # Assert
        self.assertIsNotNone(blob)


class TestDataContent(TestCase):
    """TestDataContent"""

    def test_data_content_none_returns_content(
        self,
    ):
        """test_data_content_none_returns_content

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="2", title="title", content=None
        )
        data.file = SimpleUploadedFile("test.txt", b"test")
        # Assert
        self.assertEqual(data.content, "test")

    def test_data_content_attribute_error_returns_content(
        self,
    ):
        """test_data_content_attribute_error_returns_content

        Returns:

        """
        # Arrange
        data = _create_data(
            _get_template(), user_id="2", title="title", content=None
        )
        mock_file_content = MagicMock()
        mock_file_content.read.return_value.decode.side_effect = (
            AttributeError()
        )
        data.file = mock_file_content
        # Assert
        self.assertEqual(data.content, mock_file_content.read())


class TestAbstractData(TestCase):
    class MockData(AbstractData):
        """MockData"""

        pass

    def test_convert_to_dict_raises_not_implemented_error(self):
        """test_convert_to_dict_raises_not_implemented_error

        Returns:

        """
        abs_data = TestAbstractData.MockData()
        with self.assertRaises(NotImplementedError):
            abs_data.convert_to_dict()

    def test_convert_to_file_raises_not_implemented_error(self):
        """test_convert_to_file_raises_not_implemented_error

        Returns:

        """
        abs_data = TestAbstractData.MockData()
        with self.assertRaises(NotImplementedError):
            abs_data.convert_to_file()


def _get_template():
    """Get XSD template

    Returns:

    """
    template = Template()
    template.format = Template.XSD
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    return template


def _get_json_template():
    """Get JSON template

    Returns:

    """
    template = Template()
    template.format = Template.JSON
    template.id_field = 1
    template.content = "{}"
    return template


def _create_data(template, user_id, title, content, data_id=None, blob=None):
    """Create a data

    Args:
        template:
        user_id:
        title:
        content:
        data_id:
        blob:

    Returns:

    """
    data = Data(
        template=template, user_id=user_id, title=title, id=data_id, _blob=blob
    )
    data.xml_content = content
    return data


def _create_blob(user_id, filename="test", content=b"test"):
    """Create a blob

    Returns:

    """
    return Blob(
        filename=filename,
        user_id=user_id,
        blob=SimpleUploadedFile(
            name=filename,
            content=content,
        ),
    )
