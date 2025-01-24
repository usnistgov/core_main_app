""" Upload data command
"""

import logging
import os
from argparse import BooleanOptionalAction
from glob import glob

from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.management import BaseCommand, CommandError

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.settings import XML_POST_PROCESSOR, XML_FORCE_LIST
from core_main_app.utils import xml as main_xml_utils
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.json_utils import (
    load_json_string,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Upload data from disk command"""

    help = "Load data files from file system"

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
            "--template",
            default=None,
            type=int,
            help="Id of the template for the data",
        )
        parser.add_argument(
            "--workspace",
            default=None,
            type=int,
            help="Id of workspace to assign data",
        )
        parser.add_argument(
            "--no-validation",
            default=False,
            action=BooleanOptionalAction,
            help="Validate documents",
        )
        parser.add_argument(
            "--clean-title",
            default=False,
            action=BooleanOptionalAction,
            help="Clean document title (remove extensions, underscores...)",
        )
        parser.add_argument(
            "--bulk",
            default=False,
            action=BooleanOptionalAction,
            help="Ingest document in bulk",
        )
        parser.add_argument(
            "--batch-size",
            default=10,
            type=int,
            help="Size of the batch",
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
        Setting batch to `True` will perform a bulk upload (post save signals won't be triggered).

        Parameters:
            "path": string,
            "user": integer,
            "template": integer,
            "workspace": integer,
            "batch-size": integer,
            "no-validation": boolean,
            "clean-title": boolean,
            "bulk": boolean,
            "dry-run": boolean

        Examples:
            uploaddata --path dataset/*json --template 1 --user 1 --workspace 1
            uploaddata --path dataset/*json --template 1 --user 1 --workspace 1 --dry-run
            uploaddata --path dataset/*json --template 1 --user 1 --workspace 1 --bulk --batch-size 10
            uploaddata --path dataset/*json --template 1 --user 1 --workspace 1 --no-validation --clean-title

        Args:
            args:
            options:

        """
        try:
            path = options["path"]
            user_id = options["user"]
            template_id = options["template"]
            workspace_id = options["workspace"]
            bulk = options["bulk"]
            batch_size = options["batch_size"]
            validate = not options["no_validation"]
            clean_title = options["clean_title"]
            dry_run = options["dry_run"]

            if dry_run:
                self.stdout.write("Dry run: no data will be saved.")

            if not path or not user_id or not template_id:
                raise CommandError(
                    "The following arguments are required: --path, --user, --template."
                )

            if ".." in path:
                raise CommandError("Unsupported path.")

            if bulk:
                self.stdout.write(
                    "Post-save operations will not be triggered with bulk option."
                )

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
                raise CommandError("No data found.")

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

            # Get Template
            template = Template.objects.get(id=template_id)
            self.stdout.write(
                f"Files will be assigned to template: {str(template)} (id: {template_id})"
            )

            self.stdout.write("The following files will be loaded:")
            self.stdout.write("\n".join(file_list))

            data_list = list()
            for data_file in file_list:
                try:
                    # initialize times
                    now = datetime_now()
                    # Create data
                    instance = Data(
                        template_id=template_id,
                        workspace_id=workspace_id,
                        user_id=user.id,
                        last_change_date=now,
                        creation_date=now,
                        last_modification_date=now,
                    )
                    # Set title
                    filename = os.path.split(data_file)[
                        1
                    ]  # [0] head, [1] tail (filename)
                    instance.title = (
                        filename.replace("_", " ")
                        .replace(".xml", "")
                        .replace(".json", "")
                        if clean_title
                        else data_file
                    )
                    # Set file
                    instance.file.name = data_file
                    # Validate file
                    if validate:
                        if template.format == Template.XSD:
                            data_api.check_xml_file_is_valid(instance)
                        elif template.format == Template.JSON:
                            data_api.check_json_file_is_valid(instance)
                        else:
                            raise CommandError(
                                "Unable to validate: unsupported template format."
                            )
                    # Convert to JSON
                    with open(
                        os.path.join(conf_settings.MEDIA_ROOT, data_file),
                        "rb",
                    ) as _file:
                        if template.format == Template.XSD:
                            instance.dict_content = (
                                main_xml_utils.raw_xml_to_dict(
                                    _file,
                                    postprocessor=XML_POST_PROCESSOR,
                                    force_list=XML_FORCE_LIST,
                                )
                            )
                        elif template.format == Template.JSON:
                            instance.dict_content = load_json_string(
                                _file.read()
                            )
                        else:
                            raise CommandError(
                                "Unable to convert: unsupported template format."
                            )
                    # Add data to list
                    data_list.append(instance)
                except Exception as exception:
                    self.stderr.write(
                        f"ERROR: Unable to create {data_file}: {str(exception)}"
                    )
                # If data list reaches batch size
                if len(data_list) == batch_size:
                    # Bulk insert list of data
                    if not dry_run:
                        _bulk_create(data_list, bulk)
                    # Clear list of data
                    data_list = list()
            # insert the last batch
            if not dry_run and len(data_list):
                _bulk_create(data_list, bulk)

            self.stdout.write(
                self.style.SUCCESS("Command completed. Check logs for errors.")
            )
        except DoesNotExist as dne:
            raise CommandError(f"Not found: {str(dne)}")
        except Exception as api_exception:
            raise CommandError(f"{str(api_exception)}")


def _save_list(data_list):
    """Save a list of data

    Args:
        data_list:

    Returns:

    """
    for data in data_list:
        try:
            data.save()
        except Exception as e:
            logger.error(f"Loading failed for: {data.title}. Error: {str(e)}")


def _bulk_create(data_list, bulk):
    """Bulk insert list of data

    Args:
        data_list:

    Returns:

    """
    if not bulk:
        _save_list(data_list)
        return

    try:
        # Bulk insert list of data
        Data.objects.bulk_create(data_list)
    except Exception as exception:
        # Log errors that occurred during bulk insert
        logger.error("Bulk upload failed.")
        logger.error(str(exception))
        # try inserting each data of the batch individually
        _save_list(data_list)
