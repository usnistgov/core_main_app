""" Core Exceptions
"""


class CoreError(Exception):
    """Exception raised by the Core."""

    def __init__(self, message):
        self.message = message


class ApiError(Exception):
    """Exception raised by the API."""

    def __init__(self, message):
        self.message = message


class ModelError(Exception):
    """Generic exception for the model."""

    def __init__(self, message):
        self.message = message


class RestApiError(Exception):
    """Exception raised by the the REST API."""

    def __init__(self, message):
        self.message = message


class DoesNotExist(Exception):
    """Exception raised when an object does not exist."""

    def __init__(self, message):
        self.message = message


class NotUniqueError(Exception):
    """Exception raised when an object is not unique."""

    def __init__(self, message):
        self.message = message


class XMLError(Exception):
    """Exception raised by XML validation."""

    def __init__(self, message):
        self.message = message


class XSDError(Exception):
    """Exception raised by XSD validation."""

    def __init__(self, message):
        self.message = message


class LockError(Exception):
    """Exception raised when an object is locked."""

    def __init__(self, message):
        self.message = message


class PaginationError(Exception):
    """Exception raised when an error occurs during pagination."""

    def __init__(self, message):
        self.message = message


class BlobDownloaderUrlParseError(Exception):
    """Exception raised when an error occurs during url parse."""

    def __init__(self, message):
        self.message = message


class BlobDownloaderError(Exception):
    """Exception raised when an error occurs during blob download."""

    def __init__(self, message):
        self.message = message


class SSLError(Exception):
    """Exception raised when an error occurs during SSL configuration."""

    def __init__(self, message):
        self.message = message
