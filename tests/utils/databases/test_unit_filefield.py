""" FileField unit test class
"""

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from django.utils.safestring import mark_safe

from core_main_app.utils.databases.filefield import (
    save_file_history,
    diff_files,
    file_history_display,
    delete_previous_file,
)


class TestDiffFiles(TestCase):
    """TestDiffFiles"""

    def setUp(self):
        """Setup

        Returns:

        """
        self.obj = MagicMock()
        self.obj.file_history = [{"filename": "test.json"}]
        self.obj.content = "test content"
        self.index = 0
        self.model = "model"
        self.content_field = "content"
        self.file_format = "JSON"

    def test_index_error_when_file_history_is_none(self):
        """test_index_error_when_file_history_is_none

        Returns:

        """
        # Arrange
        self.obj.file_history = None

        # Act + Assert
        with self.assertRaises(IndexError):
            diff_files(
                self.obj,
                self.index,
                self.model,
                self.content_field,
                self.file_format,
            )

    def test_index_error_when_index_is_out_of_range(self):
        """test_index_error_when_index_is_out_of_range

        Returns:

        """
        # Arrange
        self.index = 1

        # Act + Assert
        with self.assertRaises(IndexError):
            diff_files(
                self.obj,
                self.index,
                self.model,
                self.content_field,
                self.file_format,
            )

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_file_not_found_error(self, mock_core_file_storage):
        """test_file_not_found_error

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        mock_core_file_storage.return_value.open.side_effect = (
            FileNotFoundError
        )

        # Act + Assert
        with self.assertRaises(FileNotFoundError):
            diff_files(
                self.obj,
                self.index,
                self.model,
                self.content_field,
                self.file_format,
            )

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_diff_files_json(self, mock_core_file_storage):
        """test_diff_files_json

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.file_format = "JSON"
        mock_file = MagicMock()
        mock_file.read.return_value = b'{"key": "old value"}'
        mock_core_file_storage.return_value.open.return_value.__enter__.return_value = (
            mock_file
        )
        mock_core_file_storage.return_value.exists.return_value = True
        self.obj.content = '{"key": "new value"}'

        # Act
        diff = diff_files(
            self.obj, self.index, self.model, "content", self.file_format
        )

        # Assert
        self.assertEqual(
            diff,
            '\n\n  {\n<span class="diff_sub">  '
            '"key": "old value"</span>\n<span class="diff_add">  '
            '"key": "new value"</span>\n  }',
        )

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_diff_files_xml(self, mock_core_file_storage):
        """test_diff_files_xml

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.file_format = "XML"
        mock_file = MagicMock()
        mock_file.read.return_value = b"<root>old value</root>"
        mock_core_file_storage.return_value.open.return_value.__enter__.return_value = (
            mock_file
        )
        self.obj.content = "<root>new value</root>"

        # Act
        diff = diff_files(
            self.obj, self.index, self.model, "content", self.file_format
        )
        # Assert
        self.assertEqual(
            diff,
            '\n\n<span class="diff_sub">&lt;root&gt;old value&lt;/root&gt;</span>'
            '\n<span class="diff_add">'
            "&lt;root&gt;new value&lt;/root&gt;</span>",
        )


class TestSaveFileHistory(TestCase):
    """TestSaveFileHistory"""

    def setUp(self):
        """setup

        Returns:

        """
        self.obj = Mock()
        self.obj.file_history = []
        self.model = "model"

    def test_obj_without_pk(self):
        """test_obj_without_pk

        Returns:

        """
        # Arrange
        self.obj.pk = None
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertEqual(self.obj.file_history, [])

    def test_obj_without_file(self):
        """test_obj_without_file

        Returns:

        """
        # Arrange
        self.obj.pk = 1
        self.obj.file = None
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertEqual(self.obj.file_history, [])

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_file_does_not_exist_in_storage(self, mock_core_file_storage):
        """test_file_does_not_exist_in_storage

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.obj.pk = 1
        self.obj.file.name = "test.json"
        mock_core_file_storage.return_value.exists.return_value = False
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertEqual(self.obj.file_history, [])

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_file_name_already_in_history(self, mock_core_file_storage):
        """test_file_name_already_in_history

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.obj.pk = 1
        self.obj.file.name = "test.json"
        self.obj.file_history = [{"filename": "test.json"}]
        mock_core_file_storage.return_value.exists.return_value = True
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertEqual(len(self.obj.file_history), 1)

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    @patch("core_main_app.utils.databases.filefield.datetime_now")
    def test_file_name_not_in_history(
        self, mock_datetime_now, mock_core_file_storage
    ):
        """test_file_name_not_in_history

        Args:
            mock_datetime_now:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.obj.pk = 1
        self.obj.file.name = "test.json"
        self.obj.file_history = []
        mock_core_file_storage.return_value.exists.return_value = True
        mock_datetime_now.return_value.strftime.return_value = (
            "2025-01-01 12:00:00"
        )
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertEqual(len(self.obj.file_history), 1)
        self.assertEqual(self.obj.file_history[0]["filename"], "test.json")
        self.assertEqual(
            self.obj.file_history[0]["updated_at"], "2025-01-01 12:00:00"
        )

    @patch("core_main_app.utils.databases.filefield.logger")
    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_exception_occurs(self, mock_core_file_storage, mock_logger):
        """test_exception_occurs

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        self.obj.pk = 1
        self.obj.file = Mock()
        self.obj.file.name = "test.json"
        self.obj.file_history = []
        mock_core_file_storage.side_effect = Exception("Test exception")
        # Act
        save_file_history(self.obj, self.model)
        # Assert
        self.assertTrue(mock_logger.error.called)


class TestFileHistoryDisplay(TestCase):
    """TestSaveFileHistory"""

    def test_empty_file_history(self):
        """test_empty_file_history

        Returns:

        """
        # Arrange
        obj = Mock(file_history=None, id=1)
        diff_url = "admin:diff_file_data"
        delete_url = "admin:delete_file_data"
        # Act
        output = file_history_display(obj, diff_url, delete_url)
        # Assert
        self.assertEqual(output, mark_safe("No file history"))

    def test_non_empty_file_history(self):
        """test_non_empty_file_history

        Returns:

        """
        # Arrange
        obj = Mock(
            file_history=[
                {"filename": "test.json", "updated_at": "2025-01-01"}
            ],
            id=1,
        )
        diff_url = "admin:diff_file_data"
        delete_url = "admin:delete_file_data"
        # Act
        output = file_history_display(obj, diff_url, delete_url)
        expected_output = mark_safe(
            "<p>test.json (2025-01-01) "
            '<a class="default" href="/admin/core_main_app/data/diff/1/0/">Diff</a>'
            ' <a class="deletelink" '
            'href="/admin/core_main_app/data/delete_previous_file/1/0/">Delete</a><br/><p>'
        )
        # Assert
        self.assertEqual(output, expected_output)

    def test_file_history_with_no_updated_at_date(self):
        """test_file_history_with_no_updated_at_date

        Returns:

        """
        # Arrange
        obj = Mock(file_history=[{"filename": "test.json"}], id=1)
        diff_url = "admin:diff_file_data"
        delete_url = "admin:delete_file_data"
        # Act
        output = file_history_display(obj, diff_url, delete_url)
        expected_output = mark_safe(
            "<p>test.json (no date) "
            '<a class="default" href="/admin/core_main_app/data/diff/1/0/">Diff</a>'
            ' <a class="deletelink" '
            'href="/admin/core_main_app/data/delete_previous_file/1/0/">Delete</a><br/><p>'
        )
        # Assert
        self.assertEqual(output, expected_output)


class TestDeletePreviousFile(TestCase):
    """TestDeletePreviousFile"""

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_delete_previous_file_valid_index(self, mock_core_file_storage):
        """test_delete_previous_file_valid_index

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        obj = Mock(
            file_history=[
                {"filename": "test1.txt"},
                {"filename": "test2.txt"},
            ],
            pk=1,
        )
        obj.__class__.objects = Mock()
        obj.__class__.objects.filter.return_value = Mock(update=Mock())
        index = 0
        model = "model"
        # Act
        delete_previous_file(obj, index, model)
        # Assert
        mock_core_file_storage.return_value.delete.assert_called_once_with(
            "test1.txt"
        )
        self.assertEqual(obj.file_history, [{"filename": "test2.txt"}])
        obj.__class__.objects.filter.assert_called_once_with(pk=obj.pk)
        obj.__class__.objects.filter.return_value.update.assert_called_once_with(
            file_history=[{"filename": "test2.txt"}]
        )

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_delete_previous_file_out_of_range_index(
        self, mock_core_file_storage
    ):
        """test_delete_previous_file_out_of_range_index

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        obj = Mock(file_history=[{"filename": "test1.txt"}], pk=1)
        obj.__class__.objects = Mock()
        index = 1
        model = "model"
        # Act + Assert
        with self.assertRaises(IndexError):
            delete_previous_file(obj, index, model)

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_delete_previous_file_empty_file_history(
        self, mock_core_file_storage
    ):
        """test_delete_previous_file_empty_file_history

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        obj = Mock(file_history=[], pk=1)
        obj.__class__.objects = Mock()
        index = 0
        model = "model"
        # Act + Assert
        with self.assertRaises(IndexError):
            delete_previous_file(obj, index, model)

    @patch("core_main_app.utils.databases.filefield.core_file_storage")
    def test_delete_previous_file_core_file_storage_delete_fails(
        self, mock_core_file_storage
    ):
        """test_delete_previous_file_core_file_storage_delete_fails

        Args:
            mock_core_file_storage:

        Returns:

        """
        # Arrange
        mock_core_file_storage.return_value.delete.side_effect = Exception(
            "Test exception"
        )
        obj = Mock(file_history=[{"filename": "test1.txt"}], pk=1)
        obj.__class__.objects = Mock()
        index = 0
        model = "model"
        # Act + Assert
        with self.assertRaises(Exception):
            delete_previous_file(obj, index, model)
