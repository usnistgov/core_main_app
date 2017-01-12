"""
    The API contains the available function to access, create and edit a user
"""
from django.contrib.auth.models import User


def get_all_users():
    """
    Return all Users

    Returns:
        List of Users

    """
    return User.objects.all()


def get_user_by_username(username):
    """
        Returns a user given its username

        Args:
            username (str): Given username

        Returns:
            User object
    """
    return User.objects.get(username=username)


def get_user_by_id(user_id):
    """
        Returns a user given its primary key

        Args:
            user_id (str): Given user id

        Returns:
            User object
    """
    return User.objects.get(pk=user_id)


def create_and_save_user(username, password, first_name, last_name, email):
    """
        Save a user with the given parameters

        Args:
            username (str): Given user name
            password (str): Given password
            first_name (str): Given first name
            last_name (str): Given last name
            email (str): Given email

        Returns:
            User object
    """
    user = User.objects.create_user(username=username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    return upsert(user)


def upsert(user):
    """

    Args:
        user (User): The user to be saved

    Returns:

    """
    # Has to be called separately because save from django object returns nothing
    user.save()
    return user
