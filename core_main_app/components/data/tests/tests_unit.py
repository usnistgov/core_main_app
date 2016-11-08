"""
    Unit Test Data
"""
import core_main_app.components.data.api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.commons import exceptions
from unittest.case import TestCase
from mock import patch
from collections import OrderedDict


class TestDataAll(TestCase):

    @patch('core_main_app.components.data.models.Data.get_all')
    def test_data_all_return_collection_of_data(self, mock_list):
        # Arrange
        mock_data_1 = Data('1', OrderedDict(), 'title_1', '2')
        mock_data_2 = Data('1', OrderedDict(), 'title_2', '2')
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_api.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))


class TestDataGetById(TestCase):

    @patch('core_main_app.components.data.models.Data.get_by_id')
    def test_data_get_by_id_return_api_error_if_not_found(self, mock_get):
        # Arrange
        mock_get.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.get_by_id(1)

    @patch('core_main_app.components.data.models.Data.get_by_id')
    def test_data_get_by_id_return_data_if_found(self, mock_get):
        # Arrange
        mock_data = Data('1', OrderedDict(), 'title', '2')
        mock_get.return_value = mock_data
        # Act
        result = data_api.get_by_id('1')
        # Assert
        self.assertIsInstance(result, Data)


class TestDataAllByUser(TestCase):

    @patch('core_main_app.components.data.models.Data.get_all_by_user_id')
    def test_data_all_by_user_return_collection_of_data_from_user(self, mock_list_by_user_id):
        # Arrange
        user_id = '2'
        mock_data_1 = Data('1', OrderedDict(), 'title_1', user_id)
        mock_data_2 = Data('1', OrderedDict(), 'title_2', user_id)
        mock_list_by_user_id.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_api.get_all_by_user(user_id)
        # Assert
        self.assertTrue(all(item.content['user_id'] == user_id for item in result))


class TestDataAllExceptUser(TestCase):

    @patch('core_main_app.components.data.models.Data.get_all_except_user_id')
    def test_data_all_except_user_return_collection_of_data_where_user_is_not_owner(self, mock_list_except_user_id):
        # Arrange
        user_id = '2'
        mock_data_1 = Data('1', OrderedDict(), 'title_1', '3')
        mock_data_2 = Data('1', OrderedDict(), 'title_2', '1')
        mock_list_except_user_id.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_api.get_all_except_user(user_id)
        # Assert
        self.assertTrue(all(item.content['user_id'] != user_id for item in result))


class TestDataAllByIdList(TestCase):

    @patch('core_main_app.components.data.models.Data.get_all_by_id_list')
    def test_data_all_by_id_list_return_collection_of_data(self, mock_list_by_id_list):
        # Arrange
        mock_data_1 = Data('1', OrderedDict(), 'title_1', '2')
        mock_data_2 = Data('1', OrderedDict(), 'title_2', '1')
        mock_list_by_id_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_api.get_all_by_id_list([1, 2])
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch('core_main_app.components.data.models.Data.get_all_by_id_list')
    def test_data_all_by_id_list_return_collection_of_distinct_data_by_template(self, mock_list_by_id_list):
        # Arrange
        mock_data_1 = Data('1', OrderedDict(), 'title_1', '2')
        mock_list_by_id_list.return_value = [mock_data_1]
        # Act
        result = data_api.get_all_by_id_list([1], 'template_id')
        count_result = len([item.content['template_id'] == '1' for item in result])
        # Assert
        self.assertEqual(count_result, 1)


class TestDataUpdate(TestCase):

    @patch('core_main_app.utils.database.Database.connect')
    def test_date_update_raise_api_error_if_database_connection_fail(self, mock_connect):
        # Arrange
        mock_connect.side_effect = Exception()
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.update(1)

    @patch('core_main_app.components.data.models.Data.update')
    @patch('core_main_app.components.data.models.Data.get_by_id')
    def test_data_update_return_data_with_new_title_if_update_is_called_with_only_title_parameter(self, mock_get,
                                                                                                  mock_update):
        # Arrange
        mock_update.return_value = Data('1', OrderedDict(), 'toto', '2')
        mock_data = Data('1', OrderedDict(), 'title', '2')
        mock_get.return_value = mock_data
        # Act
        result = data_api.update(1, title='toto')
        # Assert
        self.assertEqual('toto', result.content['title'])

    @patch('core_main_app.components.data.models.Data.update')
    @patch('core_main_app.components.data.models.Data.get_by_id')
    def test_data_update_return_data_with_new_user_id_if_update_is_called_with_only_user_id_parameter(self, mock_get,
                                                                                                      mock_update):
        # Arrange
        mock_update.return_value = Data('1', OrderedDict(), 'title', '3')
        mock_data = Data('1', OrderedDict(), 'title', '2')
        mock_get.return_value = mock_data
        # Act
        result = data_api.update(1, user_id='3')
        # Assert
        self.assertEqual('3', result.content['user_id'])

    @patch('core_main_app.components.data.models.Data.update')
    @patch('core_main_app.components.data.models.Data.get_by_id')
    def test_data_update_return_data_with_content_if_update_is_called_with_only_content_parameter(self, mock_get,
                                                                                                  mock_upd):
        # Arrange
        mock_upd.return_value = Data('1', OrderedDict([(u'tag', u'toto')]), 'title', '2')
        mock_get.return_value = Data('1', OrderedDict(), 'title', '2')
        json = OrderedDict([(u'tag', u'toto')])
        xml = '<tag>toto</tag>'
        # Act
        result = data_api.update(1, xml_content=xml)
        # Assert
        self.assertEqual(json, result.content['content'])

    @patch('core_main_app.utils.database.Database.connect_to_collection')
    def test_date_update_data_raise_data_model_error_if_data_id_is_None(self, mock_con):
        # Arrange
        mock_con.return_value = []
        # Act # Assert
        with self.assertRaises(exceptions.DataModelError):
            Data._update_data(json_full_object={})

    @patch('core_main_app.utils.database.Database.connect_to_collection')
    def test_date_update_data_raise_data_model_error_if_content_is_None(self, mock_con):
        # Arrange
        mock_con.return_value = []
        # Act # Assert
        with self.assertRaises(exceptions.DataModelError):
            Data._update_data(data_id='1')


class TestDataSaveWithXml(TestCase):

    def test_data_save_with_xml_raise_api_error_if_xml_is_none(self):
        # Arrange
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.save_with_xml('1', None)

    @patch('core_main_app.components.data.models.Data.save')
    @patch('core_main_app.components.data.api._check_xml_data_valid')
    def test_data_save_with_xml_return_data_if_xml_is_not_none(self, mock_valid, mock_save):
        # Arrange
        mock_valid.return_value = None
        mock_save.return_value = Data('1', OrderedDict(), 'title', '2')
        xml = '<tag>toto</tag>'
        # Act
        result = data_api.save_with_xml('1', xml=xml, title='title', user_id='2')
        # Assert
        self.assertIsInstance(result, Data)

    @patch('core_main_app.components.template.api.get')
    def test_data_check_xml_data_valid_raise_xml_error_if_xml_tree_fail(self, mock_template):
        # Arrange
        template = Template()
        mock_template.return_value = template
        xml = '<tag>toto'
        # Act # Assert
        with self.assertRaisesRegexp(exceptions.XMLError, "Unexpected error: XML is not well formed."):
            data_api._check_xml_data_valid(xml, 1)

    @patch('core_main_app.components.template.api.get')
    def test_data_check_xml_data_valid_raise_xsd_error_if_xsd_tree_fail(self, mock_template):
        # Arrange
        template = Template()
        mock_template.return_value = template
        xml = '<tag>toto</tag>'
        # Act # Assert
        with self.assertRaisesRegexp(exceptions.XSDError, "Unexpected error: XSD is not well formed."):
            data_api._check_xml_data_valid(xml, 1)

    @patch('core_main_app.components.template.api.get')
    def test_data_check_xml_data_valid_raise_xml_error_if_validation_fail(self, mock_template):
        # Arrange
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        mock_template.return_value = template
        xml = '<tog>toto</tog>'
        # Act # Assert
        with self.assertRaisesRegexp(exceptions.XMLError, '^.*No matching.*$'):
            data_api._check_xml_data_valid(xml, 1)

    @patch('core_main_app.components.template.api.get')
    def test_data_check_xml_data_valid_return_none_if_validation_success(self, mock_template):
        # Arrange
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        mock_template.return_value = template
        xml = '<tag>toto</tag>'
        # Act
        result = data_api._check_xml_data_valid(xml, 1)
        # Assert
        self.assertEqual(result, None)


class TestDataSaveWithJson(TestCase):

    def test_data_save_with_json_raise_api_error_if_content_is_none(self):
        # Arrange
        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            data_api.save_with_json('1', None)

    @patch('core_main_app.components.data.models.Data.save')
    @patch('core_main_app.components.data.api._check_json_data_valid')
    def test_data_save_with_json_return_data_if_json_is_not_none(self, mock_valid, mock_save):
        # Arrange
        mock_valid.return_value = None
        mock_save.return_value = Data('1', OrderedDict(), 'title', '2')
        json = OrderedDict([(u'tag', u'toto')])
        # Act
        result = data_api.save_with_json('1', json=json, title='title', user_id='2')
        # Assert
        self.assertIsInstance(result, Data)

    @patch('core_main_app.components.template.api.get')
    def test_data_check_json_data_valid_raise_xml_error_if_validation_fail(self, mock_template):
        # Arrange
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        mock_template.return_value = template
        json = OrderedDict([(u'tog', u'toto')])
        # Act # Assert
        with self.assertRaisesRegexp(exceptions.XMLError, '^.*No matching.*$'):
            data_api._check_json_data_valid(json, '1')

    @patch('core_main_app.components.template.api.get')
    def test_data_check_json_data_valid_return_none_if_validation_success(self, mock_template):
        # Arrange
        template = Template()
        xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
              '<xs:element name="tag"></xs:element></xs:schema>'
        template.content = xsd
        mock_template.return_value = template
        json = OrderedDict([(u'tag', u'toto')])
        # Act
        result = data_api._check_json_data_valid(json, '1')
        # Assert
        self.assertEqual(result, None)


class TestDataQuery(TestCase):

    def test_data_query_raise_api_error_if_no_parameter_given(self):
        # Arrange
        # Act # Assert
        with self.assertRaisesRegexp(exceptions.ApiError, 'No parameters given.'):
            data_api.query()

    @patch('core_main_app.components.data.models.Data.find')
    def test_data_query_return_data_if_query_value_is_not_none(self, mock_find):
        # Arrange
        mock_find.return_value = Data('1', OrderedDict(), 'title', '2')
        # Act
        result = data_api.query(query_value='query')
        # Assert
        self.assertIsInstance(result, Data)

    @patch('core_main_app.components.data.models.Data.find')
    def test_data_query_return_data_if_query_value_is_none_but_data_id_is_hexa_string(self, mock_find):
        # Arrange
        mock_find.return_value = Data('1', OrderedDict(), 'title', '2')
        # Act
        result = data_api.query(data_id='507f1f77bcf86cd799439011')
        # Assert
        self.assertIsInstance(result, Data)

    @patch('core_main_app.components.data.models.Data.find')
    def test_data_query_return_data_if_query_value_is_none_but_schema_id_is_string(self, mock_find):
        # Arrange
        mock_find.return_value = Data('1', OrderedDict(), 'title', '2')
        # Act
        result = data_api.query(schema_id='2')
        # Assert
        self.assertIsInstance(result, Data)

    @patch('core_main_app.components.data.models.Data.find')
    def test_data_query_return_data_if_query_value_is_none_but_title_is_string(self, mock_find):
        # Arrange
        mock_find.return_value = Data('1', OrderedDict(), 'title', '2')
        # Act
        result = data_api.query(title='title')
        # Assert
        self.assertIsInstance(result, Data)


class TestDataQueryFullText(TestCase):

    @patch('core_main_app.components.data.models.Data.execute_full_text_query')
    def test_data_execute_full_text_query_return_collection(self, mock_execute):
        # Arrange
        mock_data_1 = Data('1', OrderedDict(), 'title_1', '2')
        mock_data_2 = Data('1', OrderedDict(), 'title_2', '2')
        mock_execute.return_value = [mock_data_1, mock_data_2]
        # Act
        result = data_api.query_full_text('', '1')
        # Assert
        self.assertTrue(all(isinstance(item, Data) for item in result))
