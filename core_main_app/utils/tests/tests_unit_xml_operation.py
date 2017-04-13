"""
    Xml operation test class
"""
import core_main_app.commons.exceptions as exceptions
from unittest import TestCase
from core_main_app.utils.xml import raw_xml_to_dict
from collections import OrderedDict


class TestRawToDict(TestCase):
    def test_raw_to_dict_valid(self):
        # Arrange
        raw_xml = '<root><test>Hello</test></root>'
        expected_dict = OrderedDict([(u'root', OrderedDict([(u'test', u'Hello')]))])

        # Act
        xml_dict = raw_xml_to_dict(raw_xml)

        # Assert
        self.assertEquals(expected_dict, xml_dict)

    def test_raw_to_dict_throws_exception_when_invalid_xml(self):
        # Arrange
        raw_xml = '<root><test>Hello</test?</root>'

        # Act # Assert
        with self.assertRaises(exceptions.XMLError):
            raw_xml_to_dict(raw_xml)

