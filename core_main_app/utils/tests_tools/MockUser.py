"""Mock user object for tests
"""


class MockUser(object):
    def __init__(self, user_id, is_staff=False):
        self.id = user_id
        self.is_staff = is_staff
