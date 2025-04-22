""" FileField unit test class
"""

from unittest import TestCase
from unittest.mock import MagicMock

from core_main_app.utils.databases.filefield import replace_file


class TestReplaceFile(TestCase):
    """Test replace_file"""

    def test_replace_file_delete_old_file(self):
        """test_replace_file_delete_old_file"""
        # Arrange
        mock_instance = MagicMock(pk=1)
        mock_instance.file = MagicMock()
        mock_old_instance = MagicMock(file=MagicMock(name="old_file.txt"))
        mock_old_instance.file.delete = MagicMock()
        mock_sender = MagicMock()
        mock_sender.objects.get.return_value = mock_old_instance

        # Act
        replace_file(sender=mock_sender, instance=mock_instance)

        # Assert
        mock_old_instance.file.delete.assert_called_once_with(save=False)

    def test_replace_file_instance_has_no_pk_does_nothing(self):
        """test_replace_file_instance_has_no_pk_does_nothing

        Returns:

        """
        # Arrange
        mock_data = MagicMock(pk=None)
        mock_sender = MagicMock()
        mock_sender.objects.get.return_value = None

        # Act
        replace_file(sender=mock_sender, instance=mock_data)

        # Assert
        self.assertFalse(mock_sender.objects.get.called)

    def test_replace_file_does_not_delete_file_if_instance_not_found(self):
        """test_replace_file_does_not_delete_file_if_instance_not_found"""
        # Arrange
        mock_instance = MagicMock(pk=1)
        mock_instance.file = MagicMock()
        mock_old_instance = MagicMock(file=MagicMock(name="old_file.txt"))
        mock_old_instance.file.delete = MagicMock()
        mock_sender = MagicMock()
        mock_sender.objects.get.side_effect = mock_sender.DoesNotExist("Error")

        # Act
        replace_file(sender=mock_sender, instance=mock_instance)

        # Assert
        self.assertFalse(mock_old_instance.file.delete.called)

    def test_replace_file_does_not_delete_file_if_error_occurs(self):
        """test_replace_file_does_not_delete_file_if_error_occurs"""
        # Arrange
        mock_instance = MagicMock(pk=1)
        mock_instance.file = MagicMock()
        mock_old_instance = MagicMock(file=MagicMock(name="old_file.txt"))
        mock_old_instance.file.delete = MagicMock()
        mock_sender = MagicMock()
        mock_sender.DoesNotExist = type("DoesNotExist", (Exception,), {})
        mock_sender.objects.get.side_effect = Exception("Error")

        # Act
        replace_file(sender=mock_sender, instance=mock_instance)

        # Assert
        self.assertFalse(mock_old_instance.file.delete.called)

    def test_replace_file_does_not_delete_file_if_same_file(self):
        """test_replace_file_does_not_delete_file_if_same_file"""
        # Arrange
        mock_instance = MagicMock(pk=1)
        mock_old_instance = MagicMock(file=MagicMock(name="old_file.txt"))

        mock_instance.file = mock_old_instance.file
        mock_old_instance.file.delete = MagicMock()
        mock_sender = MagicMock()
        mock_sender.objects.get.return_value = mock_old_instance

        # Act
        replace_file(sender=mock_sender, instance=mock_instance)

        # Assert
        self.assertFalse(mock_old_instance.file.delete.called)
