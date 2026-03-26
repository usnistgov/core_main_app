"""Allauth Adapter utils test class"""

import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.utils.allauth.signals import sync_user_saml_groups
from core_main_app.utils.tests_tools.MockUser import create_mock_user

from allauth.socialaccount.models import SocialAccount


class TestSyncUserSamlGroups(TestCase):
    """TestSyncUserSamlGroups"""

    @patch.dict(
        os.environ,
        {
            "SAML_PROVIDER_ID": "provider_id",
            "SAML_ATTRIBUTES_MAP_GROUPS": "member",
        },
    )
    @patch("allauth.socialaccount.models.SocialAccount.objects.get")
    @patch("django.contrib.auth.models.Group.objects")
    def test_sync_user_saml_groups(
        self, mock_group_objects, mock_social_account_get
    ):
        """test_sync_user_saml_groups"""
        # Arrange
        mock_user = create_mock_user("2")
        mock_user.groups = MagicMock()
        mock_user.groups.values_list.return_value = [
            "default",
            "provider_id/group1",
            "provider_id/group3",
        ]
        mock_user.groups.remove = MagicMock()
        mock_user.groups.add = MagicMock()
        mock_social_account = MagicMock(
            extra_data={"member": ["group1", "group2"]}
        )
        mock_social_account_get.return_value = mock_social_account
        mock_group = MagicMock()
        mock_group_objects.get_or_create.return_value = (mock_group, False)
        mock_group_objects.filter.return_value = [mock_group]
        mock_request = MagicMock()

        # Act
        sync_user_saml_groups(mock_request, mock_user)

        # Assert
        self.assertEqual(mock_user.groups.remove.call_count, 1)
        self.assertEqual(mock_user.groups.add.call_count, 1)

    @patch.dict(
        os.environ,
        {
            "SAML_PROVIDER_ID": "mock_provider_id",
            "SAML_ATTRIBUTES_MAP_GROUPS": "member",
        },
    )
    @patch("allauth.socialaccount.models.SocialAccount.objects.get")
    def test_sync_user_saml_groups_without_social_account(
        self, mock_social_account_get
    ):
        """test_sync_user_saml_groups_without_social_accoutn"""
        # Arrange
        mock_user = mock_user = create_mock_user("2")
        mock_social_account_get.side_effect = SocialAccount.DoesNotExist()
        mock_request = MagicMock()

        # Act
        sync_user_saml_groups(mock_request, mock_user)

        # Assert
        self.assertEqual(mock_user.groups.remove.call_count, 0)
        self.assertEqual(mock_user.groups.add.call_count, 0)
