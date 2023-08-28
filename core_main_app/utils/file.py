""" File utils
"""
import base64
import re
import pathlib
from io import BytesIO
from mimetypes import guess_type

from django.http.response import HttpResponse

from core_main_app.commons.constants import (
    DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT,
    DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
    TEMPLATE_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT,
    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
)
from core_main_app.commons.exceptions import CoreError


def get_file_http_response(
    file_content, file_name, content_type=None, extension=""
):
    """Return http response with file to download

    Args:
        file_content:
        file_name:
        content_type:
        extension:

    Returns:

    """
    try:
        # set file content
        try:
            _file = BytesIO(file_content.encode("utf-8"))
        except Exception:
            _file = BytesIO(file_content)

        # guess file content type if not set
        if content_type is None:
            # The function 'guess_type' returns a tuple (type, encoding). The
            # HttpResponse only needs the type of the file sent, otherwise it
            # cannot detect the proper content type of the file.
            #
            # See https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
            content_type = guess_type(file_name)[0]
        # set file in http response
        response = HttpResponse(_file, content_type=content_type)
        # set filename extension
        if not file_name.endswith(extension):
            if not extension.startswith("."):
                extension = "." + extension
            file_name += extension
        # set content disposition in response
        response["Content-Disposition"] = "attachment; filename=" + file_name
        # return response
        return response
    except Exception:
        raise CoreError("An unexpected error occurred.")


def read_file_content(file_path):
    """Read the content of a file

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content


def get_filename_from_response(response):
    """Get filename from HTTP response

    Args:
        response: HTTP response

    Returns:

    """
    content_disposition = response.headers.get("content-disposition")
    if not content_disposition:
        return None
    file_name = re.findall("filename=(.+)", content_disposition)
    if len(file_name) == 0:
        return None
    return file_name[0]


def get_base_64_content_from_response(response):
    """Get ascii content from HTTP response

    Args:
        response: HTTP response

    Returns:

    """
    try:
        b64_content = base64.b64encode(response.content)
        return b64_content.decode("ascii")
    except Exception:
        raise CoreError("An error occurred while decoding the response.")


def get_byte_size_from_string(content):
    """Get byte size from string

    Args:
        content:

    Returns:

    """
    return len(content.encode())


def get_file_extension(filename):
    """Return the extension from a filename

    Args:
        filename:

    Returns:

    """
    return pathlib.Path(filename).suffix


def get_data_file_content_type_for_template_format(template_format):
    """get_data_file_content_type_for_template_format

    Args:
        template_format:

    Returns:

    """
    try:
        return DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT[template_format]
    except KeyError:
        return None


def get_data_file_extension_for_template_format(template_format):
    """get_data_file_extension_for_template_format

    Args:
        template_format:

    Returns:

    """
    try:
        return DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[template_format]
    except KeyError:
        return ""


def get_template_file_content_type_for_template_format(template_format):
    """get_template_file_content_type_for_template_format

    Args:
        template_format:

    Returns:

    """
    try:
        return TEMPLATE_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT[template_format]
    except KeyError:
        return None


def get_template_file_extension_for_template_format(template_format):
    """get_template_file_extension_for_template_format

    Args:
        template_format:

    Returns:

    """
    try:
        return TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[template_format]
    except KeyError:
        return ""
