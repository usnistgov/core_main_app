""" Unit Test Data
"""
from collections import OrderedDict
from unittest.case import TestCase

from mock import patch

import core_main_app.components.data.api as data_api
from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDataGetById(TestCase):

    @patch.object(Data, 'get_by_id')
    def test_data_get_by_id_raises_api_error_if_not_found(self, mock_get):
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist('')
        mock_user = _create_user('1')
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            data_api.get_by_id(1, mock_user)

    @patch.object(Data, 'get_by_id')
    def test_data_get_by_id_return_data_if_found(self, mock_get):
        # Arrange
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get.return_value = mock_data
        mock_user = _create_user('1')
        # Act
        result = data_api.get_by_id(1, mock_user)
        # Assert
        self.assertIsInstance(result, Data)


class TestDataGetAllExceptUser(TestCase):

    @patch("core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user")
    @patch.object(Data, 'get_all_except_user_id')
    def test_data_get_all_except_user_return_collection_of_data_where_user_is_not_owner(self, mock_list_except_user_id,
                                                                                        get_all_workspaces_with_read_access_by_user):
        # Arrange
        user_id = '2'
        mock_data_1 = _create_data(_get_template(), user_id='3', title='title_1', content="")
        mock_data_2 = _create_data(_get_template(), user_id='1', title='title_2', content="")
        mock_list_except_user_id.return_value = [mock_data_1, mock_data_2]
        mock_user = _create_user('2')
        get_all_workspaces_with_read_access_by_user.return_value = []
        # Act
        with self.assertRaises(AccessControlError):
            data_api.get_all_except_user(mock_user)


class TestDataUpsert(TestCase):

    @patch.object(Data, 'convert_to_file')
    @patch.object(data_api, 'check_xml_file_is_valid')
    @patch.object(Data, 'save')
    def test_data_upsert_return_data_with_new_title_if_is_called_with_only_title_modified(self, mock_save,
                                                                                          mock_check,
                                                                                          mock_convert_file):
        # Arrange
        data = _create_data(_get_template(), user_id='2', title='new_title', content='<tag></tag>')
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = _create_user('2')
        # Act
        result = data_api.upsert(data, mock_user)
        # Assert
        self.assertEqual('new_title', result.title)

    @patch.object(Data, 'convert_to_file')
    @patch.object(data_api, 'check_xml_file_is_valid')
    @patch.object(Data, 'save')
    def test_data_upsert_return_data_with_new_user_id_if_is_called_with_only_user_id_modified(self, mock_save,
                                                                                              mock_check,
                                                                                              mock_convert_file):
        # Arrange
        data = _create_data(_get_template(), user_id='3', title='new_title', content='<tag></tag>')
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = _create_user('3')
        # Act
        result = data_api.upsert(data, mock_user)
        # Assert
        self.assertEqual('3', result.user_id)

    @patch.object(Data, 'convert_to_file')
    @patch.object(data_api, 'check_xml_file_is_valid')
    @patch.object(Data, 'save')
    def test_data_upsert_return_data_with_new_xml_if_is_called_with_only_xml_modified(self, mock_save,
                                                                                      mock_check, mock_convert_file):
        # Arrange
        xml = '<new_tag></new_tag>'
        data = _create_data(_get_template(), user_id='3', title='title', content=xml)
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = _create_user('3')
        # Act
        result = data_api.upsert(data, mock_user)
        # Assert
        self.assertEqual(xml, result.xml_content)

    @patch.object(Data, 'convert_to_file')
    @patch.object(data_api, 'check_xml_file_is_valid')
    @patch.object(Data, 'save')
    def test_data_upsert_return_data_with_last_modification_date(self, mock_save,
                                                                 mock_check, mock_convert_file):
        # Arrange
        data = _create_data(_get_template(), user_id='3', title='title', content='<tag></tag>')
        mock_save.return_value = data
        mock_check.return_value = None
        mock_convert_file.return_value = None
        mock_user = _create_user('3')
        # Act
        result = data_api.upsert(data, mock_user)
        # Assert
        self.assertIsNotNone(result.last_modification_date)

    def test_data_upsert_raises_xml_error_if_failed_during_xml_validation(self):
        # Arrange
        data = _create_data(None, user_id='3', title='title', content='')
        mock_user = _create_user('3')
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.upsert(data, mock_user)

    def test_data_upsert_raises_xsd_error_if_failed_during_xsd_validation(self):
        # Arrange
        template = _get_template()
        template.content += "<"
        data = _create_data(template, user_id='3', title='title', content='<new_tag></new_tag>')
        mock_user = _create_user('3')
        # Act # Assert
        with self.assertRaises(exceptions.XSDError):
            data_api.upsert(data, mock_user)

    def test_data_upsert_raises_xml_error_if_failed_during_validation(self):
        # Arrange
        template = _get_template()
        data = _create_data(template, user_id='3', title='title', content='<new_tag></new_tag>')
        mock_user = _create_user('3')
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.upsert(data, mock_user)


class TestDataCheckXmlFileIsValid(TestCase):

    def test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_xml_validation(self):
        # Arrange
        data = _create_data(None, user_id='3', title='title', content='')
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.check_xml_file_is_valid(data)

    def test_data_check_xml_file_is_valid_raises_xsd_error_if_failed_during_xsd_validation(self):
        # Arrange
        template = _get_template()
        template.content += "<"
        data = _create_data(template, user_id='3', title='title', content='<new_tag></new_tag>')
        # Act # Assert
        with self.assertRaises(exceptions.XSDError):
            data_api.check_xml_file_is_valid(data)

    def test_data_check_xml_file_is_valid_raises_xml_error_if_failed_during_validation(self):
        # Arrange
        template = _get_template()
        data = _create_data(template, user_id='3', title='title', content='<new_tag></new_tag>')
        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            data_api.check_xml_file_is_valid(data)

    def test_data_check_xml_data_valid_return_true_if_validation_success(self):
        # Arrange
        template = _get_template()
        data = _create_data(template, user_id='3', title='title', content='<tag>toto</tag>')
        # Act
        result = data_api.check_xml_file_is_valid(data)
        # Assert
        self.assertEqual(result, True)


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
          '<xs:element name="tag"></xs:element></xs:schema>'
    template.content = xsd
    return template


def _create_data(template, user_id, title, content):
    data = Data(template=template,
                user_id=user_id,
                title=title)
    data.xml_content = content
    return data


def _create_user(user_id):
    return create_mock_user(user_id)
