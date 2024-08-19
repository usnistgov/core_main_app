""" Unit tests for `core_main_app.utils.object` package.
"""

from unittest import TestCase
from unittest.mock import Mock, patch

from core_main_app.utils import object as object_utils


class MockObject:
    """A mock object for the purpose of the tests."""

    pass


class TestParseProperty(TestCase):
    """Unit tests for `parse_property` function."""

    @classmethod
    def setUpClass(cls):
        """setUpClass"""
        cls.mock_prop = "prop"
        cls.mock_prop_value = "mock_prop"

        cls.mock_object = MockObject()
        setattr(cls.mock_object, cls.mock_prop, cls.mock_prop_value)

        cls.mock_dict = {cls.mock_prop: cls.mock_prop_value}

    def test_dict_input_returns_dict_property(self):
        """test_dict_input_returns_dict_property"""
        self.assertEqual(
            object_utils.parse_property(self.mock_dict, self.mock_prop),
            self.mock_prop_value,
        )

    def test_object_input_returns_object_property(self):
        """test_object_input_returns_object_property"""
        self.assertEqual(
            object_utils.parse_property(self.mock_object, self.mock_prop),
            self.mock_prop_value,
        )

    @patch.object(object_utils, "logger")
    def test_dict_prop_not_existing_raises_attribute_error(self, mock_logger):
        """test_dict_prop_not_existing_raises_attribute_error"""
        with self.assertRaises(AttributeError):
            object_utils.parse_property(self.mock_dict, "non_existing_prop")

    @patch.object(object_utils, "logger")
    def test_object_prop_not_existing_raises_attribute_error(
        self, mock_logger
    ):
        """test_object_prop_not_existing_raises_attribute_error"""
        with self.assertRaises(AttributeError):
            object_utils.parse_property(self.mock_object, "non_existing_prop")

    def test_cast_fn_not_none_is_called_for_dict(self):
        """test_cast_fn_not_none_is_called_for_dict"""
        mock_cast = Mock()

        object_utils.parse_property(self.mock_dict, self.mock_prop, mock_cast)

        mock_cast.assert_called_with(self.mock_prop_value)

    def test_cast_fn_not_none_is_called_for_object(self):
        """test_cast_fn_not_none_is_called_for_object"""
        mock_cast = Mock()

        object_utils.parse_property(
            self.mock_object, self.mock_prop, mock_cast
        )

        mock_cast.assert_called_with(self.mock_prop_value)

    def test_cast_fn_not_none_returns_output_for_dict(self):
        """test_cast_fn_not_none_returns_output_for_dict"""
        mock_cast = Mock()

        self.assertEqual(
            object_utils.parse_property(
                self.mock_dict, self.mock_prop, mock_cast
            ),
            mock_cast(self.mock_prop_value),
        )

    def test_cast_fn_not_none_returns_output_for_object(self):
        """test_cast_fn_not_none_returns_output_for_object"""
        mock_cast = Mock()

        self.assertEqual(
            object_utils.parse_property(
                self.mock_object, self.mock_prop, mock_cast
            ),
            mock_cast(self.mock_prop_value),
        )

    @patch.object(object_utils, "logger")
    def test_cast_fn_exception_returns_found_value_for_dict(self, mock_logger):
        """test_cast_fn_exception_returns_found_value_for_dict"""
        mock_cast = Mock()
        mock_cast.side_effect = Exception("mock_cast_exception")

        self.assertEqual(
            object_utils.parse_property(
                self.mock_dict, self.mock_prop, mock_cast
            ),
            self.mock_prop_value,
        )

    @patch.object(object_utils, "logger")
    def test_cast_fn_exception_returns_found_value_for_object(
        self, mock_logger
    ):
        """test_cast_fn_exception_returns_found_value_for_object"""
        mock_cast = Mock()
        mock_cast.side_effect = Exception("mock_cast_exception")

        self.assertEqual(
            object_utils.parse_property(
                self.mock_object, self.mock_prop, mock_cast
            ),
            self.mock_prop_value,
        )
