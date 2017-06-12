"""File utils
"""
from io import BytesIO
from mimetypes import guess_type

from core_main_app.commons.exceptions import CoreError
from django.http.response import HttpResponse


def get_file_http_response(file_content, file_name, content_type=None, extension=''):
    """Return http response with file to download.

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
            _file = BytesIO(file_content.encode('utf-8'))
        except Exception:
            _file = BytesIO(file_content)
        # guess file content type if not set
        if content_type is None:
            content_type = guess_type(file_name)
        # set file in http response
        response = HttpResponse(_file, content_type=content_type)
        # set filename extension
        if not file_name.endswith(extension):
            if not extension.startswith("."):
                extension = "." + extension
            file_name += extension
        # set content disposition in response
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        # return response
        return response
    except Exception:
        raise CoreError('An unexpected error occurred.')


def read_file_content(file_path):
    """Read the content of a file.

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content
