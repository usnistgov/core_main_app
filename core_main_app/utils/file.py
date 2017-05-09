"""File utils
"""
from io import BytesIO

from core_main_app.commons.exceptions import CoreError
from django.http.response import HttpResponse


def get_file_http_response(file_content, file_name, content_type, extension):
    """

    Args:
        file_content:
        file_name:
        content_type:
        extension:

    Returns:

    """
    try:
        # Set file content
        try:
            _file = BytesIO(file_content.encode('utf-8'))
        except Exception:
            _file = BytesIO(file_content)
        response = HttpResponse(_file, content_type=content_type)
        if not file_name.endswith(extension):
            if not extension.startswith("."):
                extension = "." + extension
            file_name += extension
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response
    except Exception:
        raise CoreError('An unexpected error occurred.')
