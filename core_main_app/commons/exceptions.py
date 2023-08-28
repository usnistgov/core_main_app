""" Core Exceptions
"""


class BaseCoreException(Exception):
    """BaseCoreException"""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__()
        self.message = message

    def __str__(self):
        """Exception as string

        Returns:

        """
        return self.message


class CoreError(BaseCoreException):
    """Exception raised by the Core."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class ApiError(BaseCoreException):
    """Exception raised by the API."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class ModelError(BaseCoreException):
    """Generic exception for the model."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class RestApiError(BaseCoreException):
    """Exception raised by the the REST API."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class DoesNotExist(BaseCoreException):
    """Exception raised when an object does not exist."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class NotUniqueError(BaseCoreException):
    """Exception raised when an object is not unique."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class XMLError(BaseCoreException):
    """Exception raised by XML validation."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class XSDError(BaseCoreException):
    """Exception raised by XSD validation."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class JSONError(BaseCoreException):
    """Exception raised by the JSON validation."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class LockError(BaseCoreException):
    """Exception raised when an object is locked."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class PaginationError(BaseCoreException):
    """Exception raised when an error occurs during pagination."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class BlobDownloaderUrlParseError(BaseCoreException):
    """Exception raised when an error occurs during url parse."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class BlobDownloaderError(BaseCoreException):
    """Exception raised when an error occurs during blob download."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class SSLError(BaseCoreException):
    """Exception raised when an error occurs during SSL configuration."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class QueryError(BaseCoreException):
    """Exception raised when an error occurs regarding queries."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)


class DocumentEditingSizeError(BaseCoreException):
    """Exception raised when an edited document is too large."""

    def __init__(self, message):
        """Initialize exception

        Args:
            message:
        """
        super().__init__(message)
