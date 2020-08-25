"""Exceptions for access control
"""


class AccessControlError(Exception):
    """Exception raised when checking access control"""

    def __init__(self, message):
        self.message = message
