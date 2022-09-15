"""Mock user for tests
"""
from unittest.mock import Mock
from django.contrib.auth.models import User


def create_mock_user(
    user_id, is_staff=False, is_superuser=False, has_perm=False, is_anonymous=False
):
    """Mock a User.

    Args:
        user_id:
        is_staff:
        is_superuser:
        has_perm:
        is_anonymous:

    """
    mock_user = Mock(spec=User)
    mock_user.id = user_id
    mock_user.is_staff = is_staff
    mock_user.is_superuser = is_superuser
    mock_user.has_perm.return_value = has_perm
    mock_user.is_anonymous = is_anonymous

    return mock_user
