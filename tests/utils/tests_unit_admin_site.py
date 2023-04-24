""" Admin Site test class
"""
from unittest import TestCase
from unittest.mock import patch

from django.contrib.admin import ModelAdmin
from django.test import override_settings
from simple_history.admin import SimpleHistoryAdmin

from core_main_app.utils.admin_site.model_admin_class import (
    get_base_model_admin_class,
    register_simple_history_models,
)


class TestGetBaseModelAdminClass(TestCase):
    """TestGetBaseModelAdminClass"""

    @override_settings(DJANGO_SIMPLE_HISTORY_MODELS=["Data"])
    def test_get_base_model_admin_class_model_in_list(self):
        """test_get_base_model_admin_class_model_in_list

        Returns:

        """
        base_class = get_base_model_admin_class("Data")
        self.assertEquals(base_class, SimpleHistoryAdmin)

    @override_settings(DJANGO_SIMPLE_HISTORY_MODELS=["Data"])
    def test_get_base_model_admin_class_model_not_in_list(self):
        """test_get_base_model_admin_class_model_not_in_list

        Returns:

        """
        base_class = get_base_model_admin_class("Template")
        self.assertEquals(base_class, ModelAdmin)

    @override_settings(DJANGO_SIMPLE_HISTORY_MODELS=None)
    def test_get_base_model_admin_class_model_setting_not_set(self):
        """test_get_base_model_admin_class_model_setting_not_set

        Returns:

        """
        base_class = get_base_model_admin_class("Data")
        self.assertEquals(base_class, ModelAdmin)


class TestRegisterSimpleHistoryModels(TestCase):
    """TestRegisterSimpleHistoryModels"""

    @patch("simple_history.register")
    def test_register_simple_history_models_with_available_model(
        self, mock_register
    ):
        """test_register_simple_history_models_with_available_model

        Returns:

        """
        mock_register.return_value = None
        register_simple_history_models(django_simple_history_models=["Data"])
        self.assertTrue(mock_register.called)

    @patch("simple_history.register")
    def test_register_simple_history_models_with_unavailable_model(
        self, mock_register
    ):
        """test_register_simple_history_models_with_unavailable_model

        Returns:

        """
        mock_register.return_value = None
        register_simple_history_models(
            django_simple_history_models=["Template"]
        )
        self.assertFalse(mock_register.called)
