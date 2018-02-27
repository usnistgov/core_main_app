""" Fixtures files for User
"""

from django.contrib.auth.models import User

from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class UserFixtures(FixtureInterface):
    """ User Fixture
    """

    def insert_data(self):
        pass

    @staticmethod
    def create_user(username="username", password=None, email=None):
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email)
        user.save()
        return user

    @staticmethod
    def create_super_user(username="username", password="pass", email="email"):
        user = User.objects.create_superuser(username,
                                             password,
                                             email)
        user.save()
        return user