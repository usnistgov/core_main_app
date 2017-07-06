"""Exceptions for access control
"""


class AccessControlError(Exception):
    """ Exception raised when checking access control
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
