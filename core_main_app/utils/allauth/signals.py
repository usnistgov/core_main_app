"""Manage allauth signals"""

import os

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group


def sync_user_saml_groups(request, user, **kwargs):
    """Sync user groups from IdP"""
    try:
        # Get id of SAML Provider
        saml_provider_id = os.getenv("SAML_PROVIDER_ID")
        # Check if social account is from SAML provider
        social_acc = SocialAccount.objects.get(
            user=user, provider=saml_provider_id
        )
        # Get expected group attribute name from provider
        group_attr = os.getenv("SAML_ATTRIBUTES_MAP_GROUPS", "member")
        # Get value of group attribute for user from provider
        idp_groups = social_acc.extra_data.get(group_attr, [])
        idp_groups = [f"{saml_provider_id}/{group}" for group in idp_groups]

        # get current list of cdcs groups for user
        current_user_groups = set(user.groups.values_list("name", flat=True))
        # user should belong to idp groups and "default" CDCS group
        target_groups = set(idp_groups + ["default"])

        # Remove user from cdcs groups if no longer member in idp
        to_remove = current_user_groups - target_groups
        if to_remove:
            user.groups.remove(*Group.objects.filter(name__in=to_remove))

        # Add user to cdcs groups
        for group_name in target_groups - current_user_groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
    except SocialAccount.DoesNotExist:
        pass
