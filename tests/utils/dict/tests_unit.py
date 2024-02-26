""" Unit tests for `core_main_app.utils.dict package`.
"""
from unittest import TestCase

from core_main_app.utils.dict import get_dict_keys


class TestGetDictKeys(TestCase):
    """Unit tests for `get_dict_keys` function."""

    def test_all_keys_returned(self):
        """test_all_keys_returned"""
        input_dict = {"a": 1, "b": 2, "c": 3}

        self.assertEqual(get_dict_keys(input_dict), set(input_dict.keys()))

    def test_get_dict_keys_called_with_nested_dict(self):
        """test_get_dict_keys_called_with_nested_dict"""
        input_dict = {"a": 1, "b": 2, "c": {"d": 4}}
        expected_result = {"a", "b", "c", "d"}

        self.assertEqual(get_dict_keys(input_dict), expected_result)
