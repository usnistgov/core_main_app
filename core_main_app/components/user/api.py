"""
    The API contains the available function to access, create and edit a user
"""
from django.contrib.auth.models import User


def get_all_users():
    """Return all Users.

    Returns:
        List of Users

    """
    return User.objects.all()


def get_active_users():
    """Return active Users.

    Returns:
        List of active Users

    """
    return User.objects.filter(is_active=True)


def get_user_by_username(username):
    """Return a user given its username.

    Args:
        username (str): Given username

    Returns:
        User object
    """
    return User.objects.get(username=username)


def get_user_by_id(user_id):
    """Return a user given its primary key.

    Args:
        user_id (str): Given user id

    Returns:
        User object
    """
    return User.objects.get(pk=user_id)


def create_and_save_user(username, password, first_name, last_name, email):
    """Save a user with the given parameters.

    Args:
        username (str): Given user name
        password (str): Given password
        first_name (str): Given first name
        last_name (str): Given last name
        email (str): Given email

    Returns:
        User object
    """
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    return upsert(user)


def upsert(user):
    """Upsert user.

    Args:
        user (User): The user to be saved

    Returns:

    """
    # Has to be called separately because save from django object returns nothing
    user.save()
    return user


def get_all_users_except_list(list_user):
    """Get all users except the given list of users.

    Args:
        list_user

    Returns:
    """
    return get_all_users_except_list_id([str(user.id) for user in list_user])


def get_all_users_except_list_id(list_user_ids):
    """Get all users except the given list of user ids.

    Args:
        list_user_ids

    Returns:
    """
    return User.objects.exclude(id__in=list_user_ids)


def get_all_users_by_list_id(list_user_ids):
    """Get all users by the given list of user ids.

    Args:
        list_user_ids

    Returns:
    """
    return User.objects.filter(id__in=list_user_ids)


def get_id_username_dict(list_user):
    """Get a usable key-value list

    Args:
        list_user:

    Returns:

    """
    return dict((str(x.id), x.username) for x in list_user)
