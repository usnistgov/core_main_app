""" Unit tests for classes related to `core_main_app.views.user.forms.BlobFileForm`
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from core_main_app.views.user import forms as user_forms


class TestMultipleFileInput(TestCase):
    """Unit tests for `MultipleFileInput` class"""

    def test_allow_multiple_selected_is_true(self):
        """test_allow_multiple_selected_is_true"""
        self.assertTrue(user_forms.MultipleFileInput().allow_multiple_selected)


class TestMultipleFileFieldInit(TestCase):
    """Unit tests for `__init__` method of `MultipleFileField` class"""

    def setUp(self):
        self.mock_args = ()
        self.mock_kwargs = {}

    def test_kwargs_widget_default_set(self):
        """test_kwargs_widget_default_set"""
        multiple_file_field = user_forms.MultipleFileField()
        self.assertIsInstance(
            multiple_file_field.widget, user_forms.MultipleFileInput
        )

    @patch.object(user_forms.forms.FileField, "__init__")
    def test_super_init_called(self, mock_file_field):
        """test_super_init_called"""
        user_forms.MultipleFileField(*self.mock_args, **self.mock_kwargs)
        mock_file_field.assert_called_once_with(
            widget=user_forms.MultipleFileInput
        )


class TestMultipleFileFieldClean(TestCase):
    """Unit tests for `clean` method of `MultipleFileField` class"""

    def setUp(self):
        """setUp"""
        self.mock_initial = MagicMock()
        self.multiple_file_field = user_forms.MultipleFileField()

    @patch.object(user_forms.forms.FileField, "clean")
    def test_data_list_item_cleaned(self, mock_super_clean):
        """test_data_list_item_cleaned"""
        mock_file_list = ["file1", "file2"]
        self.multiple_file_field.clean(mock_file_list, self.mock_initial)

        mock_super_clean.assert_has_calls(
            [
                call("file1", self.mock_initial),
                call("file2", self.mock_initial),
            ]
        )

    @patch.object(user_forms.forms.FileField, "clean")
    def test_data_list_success_returns_data_list(self, mock_super_clean):
        """test_data_list_success_returns_data_list"""
        mock_file_list = ["file1", "file2"]
        mock_super_clean.side_effect = lambda item, initial: item

        self.assertEqual(
            self.multiple_file_field.clean(mock_file_list, self.mock_initial),
            mock_file_list,
        )

    @patch.object(user_forms.forms.FileField, "clean")
    def test_unique_data_cleaned(self, mock_super_clean):
        """test_unique_data_cleaned"""
        mock_file = "file1"
        self.multiple_file_field.clean(mock_file, self.mock_initial)

        mock_super_clean.assert_called_once_with("file1", self.mock_initial)

    @patch.object(user_forms.forms.FileField, "clean")
    def test_unique_data_success_returns_data_list(self, mock_super_clean):
        """test_unique_data_success_returns_data_list"""
        mock_file = "file1"
        mock_super_clean.side_effect = lambda item, initial: item

        self.assertEqual(
            self.multiple_file_field.clean(mock_file, self.mock_initial),
            [mock_file],
        )


class TestBlobFileForm(TestCase):
    """Unit tests for `BlobFileForm` class"""

    def test_file_is_multiple_file_field_instance(self):
        """test_file_is_multiple_file_field_instance"""
        self.assertIsInstance(
            user_forms.BlobFileForm().base_fields["file"],
            user_forms.MultipleFileField,
        )

    def test_file_widget_is_multiple_file_input_instance(self):
        """test_file_widget_is_multiple_file_input_instance"""
        self.assertIsInstance(
            user_forms.BlobFileForm().base_fields["file"].widget,
            user_forms.MultipleFileInput,
        )
