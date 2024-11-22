""" Unit tests for `rest.blob.serializers` package.
"""

from os.path import join
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import override_settings

from core_main_app.rest.blob import serializers as blob_serializers
from tests.test_settings import (
    ID_PROVIDER_SYSTEM_NAME,
    SERVER_URI,
    INSTALLED_APPS,
)


class TestBlobSerializerGetPid(TestCase):
    """Unit tests for `BlobSerializer.get_pid` method."""

    def setUp(self):
        """setUp"""

        self.mock_serializer = blob_serializers.BlobSerializer()
        self.mock_kwargs = {"instance": MagicMock()}

    @patch.object(blob_serializers, "settings")
    def test_core_linked_records_not_installed_return_none(
        self, mock_settings
    ):
        """test_core_linked_records_not_installed_return_none"""
        mock_settings.INSTALLED_APPS = []

        self.assertIsNone(self.mock_serializer.get_pid(**self.mock_kwargs))

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_auto_set_pid_false_return_none(self, mock_pid_settings):
        """test_auto_set_pid_false_return_none"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = False

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        self.assertIsNone(self.mock_serializer.get_pid(**self.mock_kwargs))

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch.object(blob_serializers, "reverse")
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_reverse_fn_called(self, mock_pid_settings, mock_reverse):
        """test_reverse_fn_called"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = True

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        self.mock_serializer.get_pid(**self.mock_kwargs)

        mock_reverse.assert_called_with(
            "core_linked_records_provider_record",
            kwargs={"provider": ID_PROVIDER_SYSTEM_NAME, "record": ""},
        )

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch("core_linked_records_app.system.blob.api")
    @patch.object(blob_serializers, "reverse")
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_get_pid_for_blob_called(
        self,
        mock_pid_settings,
        mock_reverse,
        mock_linked_records_blob_system_api,
    ):
        """test_get_pid_for_blob_called"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = True

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        self.mock_serializer.get_pid(**self.mock_kwargs)

        mock_linked_records_blob_system_api.get_pid_for_blob.assert_called_with(
            str(self.mock_kwargs["instance"].id)
        )

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch("core_linked_records_app.system.blob.api")
    @patch.object(blob_serializers, "reverse")
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_get_pid_for_blob_exception_returns_none(
        self,
        mock_pid_settings,
        mock_reverse,
        mock_linked_records_blob_system_api,
    ):
        """test_get_pid_for_blob_exception_returns_none"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = True

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        mock_linked_records_blob_system_api.get_pid_for_blob.side_effect = Exception(
            "mock_linked_records_blob_system_api_get_pid_for_blob_exception"
        )

        self.assertIsNone(self.mock_serializer.get_pid(**self.mock_kwargs))

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch.object(blob_serializers, "urljoin")
    @patch("core_linked_records_app.system.blob.api")
    @patch.object(blob_serializers, "reverse")
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_url_join_called(
        self,
        mock_pid_settings,
        mock_reverse,
        mock_linked_records_blob_system_api,
        mock_urljoin,
    ):
        """test_url_join_called"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = True

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        mock_reverse_return_value = "mock_reverse_return_value"
        mock_reverse.return_value = mock_reverse_return_value

        mock_blob_pid = MagicMock()
        mock_linked_records_blob_system_api.get_pid_for_blob.return_value = (
            mock_blob_pid
        )

        self.mock_serializer.get_pid(**self.mock_kwargs)

        mock_urljoin.assert_called_with(
            SERVER_URI,
            join(mock_reverse_return_value, mock_blob_pid.record_name),
        )

    @override_settings(
        INSTALLED_APPS=INSTALLED_APPS + ["core_linked_records_app"]
    )
    @patch.object(blob_serializers, "urljoin")
    @patch("core_linked_records_app.system.blob.api")
    @patch.object(blob_serializers, "reverse")
    @patch(
        "core_linked_records_app.components.pid_settings.models.PidSettings"
    )
    def test_success_returns_pid_value(
        self,
        mock_pid_settings,
        mock_reverse,
        mock_linked_records_blob_system_api,
        mock_urljoin,
    ):
        """test_success_returns_pid_value"""
        mock_pid_settings_obj = MagicMock()
        mock_pid_settings_obj.auto_set_pid = True

        mock_pid_settings.get.return_value = mock_pid_settings_obj

        mock_urljoin_return_value = "mock_urljoin_return_value"
        mock_urljoin.return_value = mock_urljoin_return_value

        self.assertEqual(
            self.mock_serializer.get_pid(**self.mock_kwargs),
            mock_urljoin_return_value,
        )
