""" Unit tests of get_attribute templatetag
"""
from unittest.case import TestCase

from core_main_app.templatetags.get_attribute import get_attribute


class TestObject(object):
    test = "test"


class TestSystemGetAllExcept(TestCase):
    def test_get_attribute_on_empty_object(self):
        result = get_attribute({}, "test")
        self.assertEqual(result, "")

    def test_get_attribute_on_none(self):
        result = get_attribute(None, "test")
        self.assertEqual(result, "")

    def test_get_attribute_on_object(self):
        test_obj = TestObject()
        result = get_attribute(test_obj, "test")
        self.assertEqual(result, "test")

    def test_get_attribute_on_dict(self):
        test_dict = {"test": "test"}
        result = get_attribute(test_dict, "test")
        self.assertEqual(result, "test")

    def test_get_attribute_on_table(self):
        test_tab = ["test"]
        result = get_attribute(test_tab, "0")
        self.assertEqual(result, "test")
