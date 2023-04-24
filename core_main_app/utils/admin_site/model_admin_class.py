""" Constant for admin site
"""
from django.contrib import admin
from django.conf import settings


def get_base_model_admin_class(model):
    """Return base model admin class (using simple history or not)

    Args:
        model:

    Returns:

    """
    django_simple_history_models = getattr(
        settings, "DJANGO_SIMPLE_HISTORY_MODELS", None
    )
    if django_simple_history_models and isinstance(
        django_simple_history_models, list
    ):
        # if model found in settings
        if model in django_simple_history_models:
            from simple_history.admin import SimpleHistoryAdmin

            # use simple history
            return SimpleHistoryAdmin
    # otherwise use django model admin
    return admin.ModelAdmin


def register_simple_history_models(django_simple_history_models):
    """Register models for Django simple history

    Args:
        django_simple_history_models:

    Returns:

    """
    if django_simple_history_models and isinstance(
        django_simple_history_models, list
    ):
        from simple_history import register

        if "Data" in django_simple_history_models:
            from core_main_app.components.data.models import Data

            register(Data)
