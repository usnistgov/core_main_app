""" Unit tests of system API
"""
from collections import OrderedDict
from unittest.case import TestCase

from mock import patch

import core_main_app.system.api as system_api
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
          '<xs:element name="tag"></xs:element></xs:schema>'
    template.content = xsd
    return template


class TestSystemGetAllExcept(TestCase):

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_return_data_object(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_return_correct_count(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertEqual(len(result), 1)

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_empty_list_return_data_object(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except([])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_empty_list_return_correct_count(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except([])
        self.assertEqual(len(result), 1)

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_inexistant_id_return_data_object(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, 'get_all_except')
    def test_system_get_all_except_inexistant_id_return_correct_count(self, mock_get_all_except):
        mock_data = Data(template=_get_template(), user_id='1', dict_content=OrderedDict(),
                         title='title')
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertEqual(len(result), 1)
