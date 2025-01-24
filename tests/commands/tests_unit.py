"""Command unit testing
"""

from io import StringIO
from unittest.case import TestCase
from unittest.mock import patch, MagicMock, mock_open

from django.contrib.auth.models import User
from django.core.management import call_command, CommandError

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.blob.models import Blob
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace


class TestUploadDataCommand(TestCase):
    """Test Upload Data command"""

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 2)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_raises_error_if_no_validation_implemented_for_given_format(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_raises_error_if_no_validation_implemented_for_given_format

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="Unknown")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            stdout=out,
            stderr=err,
        )
        self.assertIn(
            "Unable to validate: unsupported template format.", err.getvalue()
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_raises_error_if_no_conversion_implemented_for_given_format(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_raises_error_if_no_conversion_implemented_for_given_format

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="Unknown")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            no_validation=True,
            template=1,
            stdout=out,
            stderr=err,
        )
        self.assertIn(
            "Unable to convert: unsupported template format.", err.getvalue()
        )

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_in_workspace_checks_workspace_exists(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save_in_workspace_checks_workspace_exists

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            workspace=1,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 2)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)
        self.assertTrue(mock_workspace_objects.get.call_count == 1)

    def test_upload_data_raises_command_error_if_path_missing(
        self,
    ):
        """test_upload_data_raises_command_error_if_path_missing

        Args:

        Returns:

        """
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                user=1,
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn(
                "The following arguments are required: --path, --user, --template.",
                err.getvalue(),
            )

    def test_upload_data_raises_command_error_if_user_missing(
        self,
    ):
        """test_upload_data_raises_command_error_if_user_missing

        Args:

        Returns:

        """
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="dataset",
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn(
                "The following arguments are required: --path, --user, --template.",
                err.getvalue(),
            )

    def test_upload_data_raises_command_error_if_template_missing(
        self,
    ):
        """test_upload_data_raises_command_error_if_template_missing

        Args:

        Returns:

        """
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="dataset",
                user=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn(
                "The following arguments are required: --path, --user, --template.",
                err.getvalue(),
            )

    def test_upload_data_raises_command_error_if_unsupported_path(
        self,
    ):
        """test_upload_data_raises_command_error_if_unsupported_path

        Args:

        Returns:

        """
        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="../dataset",
                user=1,
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn("Unsupported path.", err.getvalue())

    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_raises_command_error_if_files_not_found(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
    ):
        """test_upload_data_raises_command_error_if_files_not_found

        Args:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.side_effect = Exception()

        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="dataset",
                user=1,
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn("No data found.", err.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_bulk_create(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_bulk_create

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            bulk=True,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 0)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 1)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_bulk_create_with_batch_size(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_bulk_create_with_batch_size

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            bulk=True,
            batch_size=1,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 0)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 2)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_not_called_when_dry_run(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save_not_called_when_dry_run

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            dry_run=True,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 0)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_bulk_create_not_called_when_dry_run(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_bulk_create_not_called_when_dry_run

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            dry_run=True,
            bulk=True,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 0)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_json_validation_called_when_json(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
        check_xml_file_is_valid,
        check_json_file_is_valid,
    ):
        """test_upload_data_save

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(check_json_file_is_valid.called)
        self.assertFalse(check_xml_file_is_valid.called)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch("builtins.open", new_callable=mock_open, read_data=b"<tag></tag>")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_xml_validation_called_when_xml(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
        check_xml_file_is_valid,
        check_json_file_is_valid,
    ):
        """test_upload_data_save

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.xml", "data_2.xml"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="XSD")

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertFalse(check_json_file_is_valid.called)
        self.assertTrue(check_xml_file_is_valid.called)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_not_in_storage_fails(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save_not_in_storage_fails

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data1.json", "data2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = False
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploaddata", path="images/*", user=1, stdout=out, stderr=err
            )

        self.assertTrue(mock_data_save.call_count == 0)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_raises_command_error_if_object_not_found(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save_raises_command_error_if_object_not_found

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.side_effect = DoesNotExist("error")

        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="dataset",
                user=1,
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )
            self.assertIn("Not found", err.getvalue())

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_save_raises_command_error_if_error_occurs(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_save_raises_command_error_if_error_occurs

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.side_effect = Exception()

        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command(
                "uploaddata",
                path="dataset",
                user=1,
                template=1,
                no_validation=True,
                stdout=out,
                stderr=err,
            )

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_calls_save_if_bulk_fails(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_calls_save_if_bulk_fails

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")
        mock_data_objects.bulk_create.side_effect = Exception()

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            bulk=True,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 2)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 1)

    @patch("builtins.open", new_callable=mock_open, read_data=b"{}")
    @patch.object(Data, "objects")
    @patch.object(Data, "save")
    @patch.object(Template, "objects")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploaddata.default_storage")
    @patch("core_main_app.management.commands.uploaddata.os.path.isfile")
    @patch("core_main_app.management.commands.uploaddata.glob")
    def test_upload_data_logs_error_if_save_fails(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_template_objects,
        mock_data_save,
        mock_data_objects,
        mock_file,
    ):
        """test_upload_data_logs_error_if_save_fails

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:
            mock_template_objects:
            mock_data_save:
            mock_data_objects:
            mock_file:

        Returns:

        """
        mock_glob.return_value = ["data_1.json", "data_2.json"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_template_objects.get.return_value = MagicMock(format="JSON")
        mock_data_save.side_effect = Exception()

        out = StringIO()
        err = StringIO()
        call_command(
            "uploaddata",
            path="dataset",
            user=1,
            template=1,
            no_validation=True,
            stdout=out,
            stderr=err,
        )
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_data_save.call_count == 2)
        self.assertTrue(mock_data_objects.bulk_create.call_count == 0)


class TestUploadBlobCommand(TestCase):
    """Test Upload Blob command"""

    @patch.object(Blob, "save")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_save(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_blob_save,
    ):
        """test_upload_blob_save

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()
        call_command(
            "uploadblob", path="images/*", user=1, stdout=out, stderr=err
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_blob_save.call_count == 2)

    @patch.object(Blob, "save")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_save_dry_run_does_not_call_save(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_blob_save,
    ):
        """test_upload_blob_save_dry_run_does_not_call_save

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()
        call_command(
            "uploadblob",
            path="images/*",
            user=1,
            dry_run=True,
            stdout=out,
            stderr=err,
        )
        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_blob_save.call_count == 0)

    @patch.object(Blob, "save")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_file_not_in_storage_fails(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_blob_save,
    ):
        """test_upload_blob_file_not_in_storage_fails

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = False
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploadblob", path="images/*", user=1, stdout=out, stderr=err
            )

        self.assertTrue(mock_blob_save.call_count == 0)

    @patch.object(Blob, "save")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_file_with_workspace_id_checks_workspace_exists(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_blob_save,
    ):
        """test_upload_blob_file_with_workspace_id_checks_workspace_exists

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()

        call_command(
            "uploadblob",
            path="images/*",
            user=1,
            workspace=1,
            stdout=out,
            stderr=err,
        )

        self.assertTrue(not err.getvalue())
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_workspace_objects.get.call_count == 1)
        self.assertTrue(mock_blob_save.call_count == 2)

    def test_upload_blob_without_path_raises_command_error(
        self,
    ):
        """test_upload_blob_without_path_raises_command_error

        Args:


        Returns:

        """
        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command("uploadblob", user=1, stdout=out, stderr=err)
            self.assertIn(
                "The following arguments are required: --path, --user.",
                err.getvalue(),
            )

    def test_upload_blob_without_user_raises_command_error(
        self,
    ):
        """test_upload_blob_without_user_raises_command_error

        Args:


        Returns:

        """
        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command("uploadblob", path="image/*", stdout=out, stderr=err)
            self.assertIn(
                "The following arguments are required: --path, --user.",
                err.getvalue(),
            )

    def test_upload_blob_with_invalid_path_raises_command_error(
        self,
    ):
        """test_upload_blob_with_invalid_path_raises_command_error

        Args:


        Returns:

        """
        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command(
                "uploadblob", path="../image/*", user=1, stdout=out, stderr=err
            )
            self.assertIn(
                "Unsupported path.",
                err.getvalue(),
            )

    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_save_raise_command_error_if_a_file_lookup_error_occurs(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
    ):
        """test_upload_blob_save_raise_command_error_if_a_file_lookup_error_occurs

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.side_effect = Exception()

        out = StringIO()
        err = StringIO()
        with self.assertRaises(CommandError):
            call_command(
                "uploadblob", path="images/*", user=1, stdout=out, stderr=err
            )
            self.assertIn("No files found.", err.getvalue())

    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_save_raise_command_error_if_orm_error_occurs(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
    ):
        """test_upload_blob_save_raise_command_error_if_orm_error_occurs

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.side_effect = Exception()
        mock_workspace_objects.return_value = MagicMock()

        out = StringIO()
        err = StringIO()

        with self.assertRaises(CommandError):
            call_command(
                "uploadblob", path="images/*", user=1, stdout=out, stderr=err
            )

    @patch.object(Blob, "save")
    @patch.object(Workspace, "objects")
    @patch.object(User, "objects")
    @patch("core_main_app.management.commands.uploadblob.default_storage")
    @patch("core_main_app.management.commands.uploadblob.os.path.isfile")
    @patch("core_main_app.management.commands.uploadblob.glob")
    def test_upload_blob_logs_error_if_blob_save_fails(
        self,
        mock_glob,
        mock_isfile,
        mock_default_storage,
        mock_user_objects,
        mock_workspace_objects,
        mock_blob_save,
    ):
        """test_upload_blob_logs_error_if_blob_save_fails

        Args:
            mock_glob:
            mock_isfile:
            mock_default_storage:
            mock_user_objects:
            mock_workspace_objects:

        Returns:

        """
        mock_glob.return_value = ["image1.jpg", "image2.jpg"]
        mock_isfile.return_value = True
        mock_default_storage.exists.return_value = True
        mock_user_objects.get.return_value = MagicMock()
        mock_workspace_objects.return_value = MagicMock()
        mock_blob_save.side_effect = Exception()

        out = StringIO()
        err = StringIO()
        call_command(
            "uploadblob", path="images/*", user=1, stdout=out, stderr=err
        )
        self.assertIn(
            "Command completed. Check logs for errors.", out.getvalue()
        )
        self.assertTrue(mock_blob_save.call_count == 2)
