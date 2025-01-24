""" Upload blob command
"""

import logging
import os
from argparse import BooleanOptionalAction
from glob import glob

from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.management import BaseCommand, CommandError

from core_main_app.components.blob.models import Blob
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.datetime import datetime_now

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Upload files from disk command"""

    help = "Load blob files from file system"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path", default=None, type=str, help="Path to files"
        )
        parser.add_argument(
            "--user",
            default=None,
            type=str,
            help="Id of user that will own the data",
        )
        parser.add_argument(
            "--workspace",
            default=None,
            type=int,
            help="Id of workspace to assign data",
        )
        parser.add_argument(
            "--dry-run",
            default=False,
            action=BooleanOptionalAction,
            help="Dry run",
        )

    def handle(self, *args, **options):
        """Bulk upload files at a given path.

        Dataset needs to be placed in the MEDIA_ROOT folder.
        The folder parameter is a relative path from the MEDIA_ROOT.

        Parameters:
            "path": string,
            "user": integer,
            "workspace": integer,
            "dry-run": boolean

        Examples:
            uploadblob --path images/*jpg --user 1
            uploadblob --path images/*jpg --user 1 --workspace 1
            uploadblob --path images/*jpg --user 1 --workspace 1 --dry-run

        Args:
            args:
            options:

        """
        try:
            path = options["path"]
            user_id = options["user"]
            workspace_id = options["workspace"]
            dry_run = options["dry_run"]

            if dry_run:
                self.stdout.write("Dry run: no data will be saved.")

            if not path or not user_id:
                raise CommandError(
                    "The following arguments are required: --path, --user."
                )

            if ".." in path:
                raise CommandError("Unsupported path.")

            try:
                file_list = [
                    f
                    for f in glob(
                        pathname=path,
                        root_dir=conf_settings.MEDIA_ROOT,
                    )
                    if os.path.isfile(
                        os.path.join(conf_settings.MEDIA_ROOT, f)
                    )
                    and default_storage.exists(f)
                ]
            except Exception as exc:
                self.stderr.write(str(exc))
                file_list = []

            if not file_list:
                raise CommandError("No files found.")

            # Get User
            user = User.objects.get(id=user_id)
            self.stdout.write(
                f"Files will be assigned to user: {str(user)} (id: {user_id})"
            )

            # Get Workspace
            if workspace_id:
                workspace = Workspace.objects.get(id=workspace_id)
                self.stdout.write(
                    f"Files will be assigned to workspace: {str(workspace)} (id: {workspace_id})"
                )

            self.stdout.write("The following files will be loaded:")
            self.stdout.write("\n".join(file_list))

            blob_list = list()
            for blob_file in file_list:
                try:
                    # Create blob
                    instance = Blob(
                        workspace_id=workspace_id,
                        user_id=user.id,
                        creation_date=datetime_now(),
                        filename=os.path.split(blob_file)[
                            1
                        ],  # [0] head, [1] tail (filename)
                    )
                    # Set Blob
                    instance.blob.name = blob_file

                    # save blob
                    if not dry_run:
                        instance.save()
                    blob_list.append(instance)
                except Exception as exception:
                    self.stderr.write(
                        f"ERROR: Unable to create {blob_file}: {str(exception)}"
                    )
            self.stdout.write(
                self.style.SUCCESS("Command completed. Check logs for errors.")
            )
        except Exception as api_exception:
            raise CommandError(f"{str(api_exception)}")
