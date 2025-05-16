""" FileField utils
"""

import json
import logging
from difflib import Differ
from xml.sax.saxutils import escape

from django.urls import reverse
from django.utils.safestring import mark_safe

from core_main_app.utils import xml as main_xml_utils
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.json_utils import load_json_string
from core_main_app.utils.storage.storage import core_file_storage

logger = logging.getLogger(__name__)


def diff_files(obj, index, model, content_field, file_format):
    """Get diff between current file and history file

    Args:
        obj: Object to get the history from.
        index: Index of the history to compare with.
        model: Model of the object.
        content_field: Field of the model that contains the file content.
        file_format: Format of the file.
    Returns:
        String representing the diff between the files.

    """
    if obj.file_history is None or index >= len(obj.file_history):
        raise IndexError("Index out of range")
    # Read the current file
    current_file_content = getattr(obj, content_field)
    # Read the file from history
    file_path = obj.file_history[index]["filename"]
    try:
        with core_file_storage(model=model).open(file_path, "rb") as file:
            history_file_content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("File not found")

    # Format files
    formatted_history = history_file_content
    formatted_current = current_file_content
    if file_format in ["XML", "XSD"]:
        # Pretty print XML content
        formatted_history = main_xml_utils.format_content_xml(
            history_file_content
        )
        formatted_current = main_xml_utils.format_content_xml(
            current_file_content
        )
    elif file_format == "JSON":
        # Pretty print JSON content
        formatted_history = json.dumps(
            load_json_string(history_file_content.strip()), indent=2
        )
        formatted_current = json.dumps(
            load_json_string(current_file_content.strip()), indent=2
        )
    # Compute the diff between the two formatted contents
    differ = Differ()
    diff = differ.compare(
        formatted_history.splitlines(),
        formatted_current.splitlines(),
    )
    # Format the diff
    formatted_diff = ["\n"]
    for line in diff:
        if line.startswith("+ "):
            formatted_diff.append(
                '<span class="diff_add">%s</span>'
                % escape(line.replace("+ ", "", 1))
            )
        elif line.startswith("- "):
            formatted_diff.append(
                '<span class="diff_sub">%s</span>'
                % escape(line.replace("- ", "", 1))
            )
        elif line.startswith("? "):
            continue
        else:
            formatted_diff.append(escape(line))
    return "\n".join(formatted_diff)


def file_history_display(obj, diff_url, delete_url):
    """Display file history

    Args:
        obj: Object containing file history.
        diff_url: URL used to generate diff between two files.
        delete_url: URL used to delete a file from history.
    Returns:
        HTML representation of the file history.

    """
    file_history = obj.file_history if obj.file_history else []
    output = "<p>"
    for i, file_info in enumerate(file_history):
        output += f'{file_info["filename"]} ({file_info.get("updated_at", "no date")})'
        output += f' <a class="default" href="{reverse(diff_url, args=[obj.id, i])}">Diff</a>'
        output += f' <a class="deletelink" href="{reverse(delete_url, args=[obj.id, i])}">Delete</a><br/>'
    output += "<p>"
    if not file_history:
        output = "No file history"
    return mark_safe(output)


def save_file_history(obj, model):
    """Save file history

    Args:
        obj: Object to save history for.
        model: Model of the object.
    Returns:
        None
    """
    try:
        if (
            obj.pk
            and obj.file
            and core_file_storage(model).exists(obj.file.name)
            and obj.file.name
            not in [history["filename"] for history in obj.file_history]
        ):
            # Append new file history
            obj.file_history.append(
                {
                    "filename": obj.file.name,
                    "updated_at": datetime_now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
    except Exception as exc:
        # Log any exceptions that occur during file history saving
        logger.error(
            "An error occurred while saving file history: " + str(exc)
        )


def delete_previous_file(obj, index, model):
    """Delete file from history

    Args:
        obj: Object to delete file from.
        index: Index of the file to delete.
        model: Model of the object.
    Returns:
        None
    """
    # Get file at index
    file_path = obj.file_history[index]["filename"]
    # Remove file from storage
    core_file_storage(model=model).delete(file_path)
    # Remove file from file history
    obj.file_history = (
        obj.file_history[:index] + obj.file_history[index + 1 :]  # noqa: E203
    )
    # Update the file_history field (update does not call signals)
    obj.__class__.objects.filter(pk=obj.pk).update(
        file_history=obj.file_history
    )
