"""Mock user for tests
"""
from unittest.mock import Mock

from django.contrib.auth.models import User


def create_mock_user(
    user_id,
    is_staff=False,
    is_superuser=False,
    has_perm=False,
    is_anonymous=False,
    is_active=True,
):
    """Mock a User.

    Args:
        user_id:
        is_staff:
        is_superuser:
        has_perm:
        is_anonymous:
        is_active:

    """
    mock_user = Mock(spec=User)
    mock_user.id = user_id
    mock_user.is_staff = is_staff
    mock_user.is_superuser = is_superuser
    mock_user.has_perm.return_value = has_perm
    mock_user.is_anonymous = is_anonymous
    mock_user.is_active = is_active
    mock_user.is_authenticated = True if not is_anonymous else False
    if mock_user.is_anonymous:
        mock_user.id = None
        mock_user.is_active = False

    return mock_user
