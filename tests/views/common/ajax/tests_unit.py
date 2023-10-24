""" Unit tests for `core_main_app.views.common.ajax` package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.views.common import ajax as main_common_ajax


class TestDeleteObjectModalViewFormValid(TestCase):
    """Unit tests for `DeleteObjectModalView.form_valid` method."""

    def setUp(self):
        """setUp"""
        self.mock_delete_modal = main_common_ajax.DeleteObjectModalView()
        self.mock_kwargs = {"form": MagicMock()}

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_get_object_called(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_get_object_called"""
        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_get_object.assert_called()

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_get_object_error_calls_messages_error(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_get_object_error_calls_messages_error"""
        mock_exception = "mock_get_object_exception"
        mock_request = MagicMock()

        self.mock_delete_modal.request = mock_request
        mock_get_object.side_effect = Exception(mock_exception)

        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_messages.error.assert_called_with(mock_request, mock_exception)

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_delete_called(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_delete_called"""
        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_delete.assert_called_with(self.mock_kwargs["form"])

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_delete_error_calls_messages_error(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_delete_error_calls_messages_error"""
        mock_exception = "mock_delete_exception"
        mock_request = MagicMock()

        self.mock_delete_modal.request = mock_request
        mock_delete.side_effect = Exception(mock_exception)

        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_messages.error.assert_called_with(mock_request, mock_exception)

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_success_message_not_none_calls_messages_success(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_success_message_not_none_calls_messages_success"""
        mock_success_message = "mock_success_message"
        mock_request = MagicMock()

        self.mock_delete_modal.request = mock_request
        self.mock_delete_modal.success_message = mock_success_message

        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_messages.success.assert_called_with(
            mock_request, mock_success_message
        )

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_get_success_url_called(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_get_success_url_called"""
        self.mock_delete_modal.form_valid(**self.mock_kwargs)

        mock_get_success_url.assert_called()

    @patch.object(main_common_ajax, "JsonResponse")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_success_url")
    @patch.object(main_common_ajax, "messages")
    @patch.object(main_common_ajax.DeleteObjectModalView, "_delete")
    @patch.object(main_common_ajax.DeleteObjectModalView, "get_object")
    def test_returns_json_response(
        self,
        mock_get_object,
        mock_delete,
        mock_messages,
        mock_get_success_url,
        mock_json_response,
    ):
        """test_returns_json_response"""
        mock_json_response_return_value = MagicMock()
        mock_json_response.return_value = mock_json_response_return_value

        self.assertEqual(
            self.mock_delete_modal.form_valid(**self.mock_kwargs),
            mock_json_response_return_value,
        )

        mock_json_response.assert_called_with({"url": mock_get_success_url()})


class TestDeleteObjectModalViewDelete(TestCase):
    """Unit tests for `DeleteObjectModalView._delete` method."""

    def setUp(self):
        """setUp"""
        self.mock_delete_modal = main_common_ajax.DeleteObjectModalView()
        self.mock_kwargs = {"form": MagicMock()}

    @patch.object(main_common_ajax, "super")
    def test_super_form_valid_called(self, mock_super):
        """test_super_form_valid_called"""
        self.mock_delete_modal._delete(**self.mock_kwargs)

        mock_super().form_valid.assert_called_with(self.mock_kwargs["form"])
