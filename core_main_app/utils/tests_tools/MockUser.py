"""Mock user object for tests
"""


class MockUser(object):
    """ MockUser class
    """
    def __init__(self, user_id, is_staff=False, is_superuser=False):
        """Initialize a MockUser.

        Args:
            user_id:
            is_staff:
            is_superuser:
        """
        self.id = user_id
        self.is_staff = is_staff
        self.is_superuser = is_superuser
