""" Fixtures files for User
"""
from django.contrib.auth.models import User

from core_main_app.permissions import api as permissions_api
from core_main_app.permissions import rights
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class UserFixtures(FixtureInterface):
    """User Fixture"""

    def insert_data(self):
        """insert data

        Returns:

        """
        pass

    @staticmethod
    def create_user(
        username="username", password=None, email=None, is_staff=False
    ):
        """create user

        Args:
            username:
            password:
            email:
            is_staff:

        Returns:

        """
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=is_staff,
        )
        user.save()
        return user

    @staticmethod
    def create_super_user(username="username", password="pass", email="email"):
        """create super user

        Args:
            username:
            password:
            email:

        Returns:

        """
        user = User.objects.create_superuser(username, password, email)
        user.save()
        return user

    @staticmethod
    def add_publish_perm(user):
        """add publish perm

        Args:
            user:

        Returns:

        """
        publish_perm = permissions_api.get_by_codename(rights.PUBLISH_DATA)
        user.user_permissions.add(publish_perm)
        user.save()
