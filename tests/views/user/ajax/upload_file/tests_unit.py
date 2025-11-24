"""Unit tests for `UploadFile` view at `core_main_app.views.user.ajax`."""

import json
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from rest_framework import status

from core_main_app.views.user import ajax as user_ajax


class TestUploadFilePost(TestCase):
    """Unit tests for `post` method of `UploadFile` class-based view."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"request": MagicMock()}
        self.upload_file_cls = user_ajax.UploadFile()

    @patch.object(user_ajax, "BlobFileForm")
    def test_blob_file_form_instantiated(self, mock_blob_file_form):
        """test_blob_file_form_instantiated"""
        self.upload_file_cls.post(**self.mock_kwargs)

        mock_blob_file_form.assert_called_once_with(
            self.mock_kwargs["request"].POST, self.mock_kwargs["request"].FILES
        )

    @patch.object(user_ajax, "BlobFileForm")
    def test_blob_file_form_exception_returns_http_400(
        self, mock_blob_file_form
    ):
        """test_blob_file_form_exception_returns_http_400"""
        mock_blob_file_form.side_effect = Exception(
            "mock_blob_file_form_exception"
        )

        self.assertEqual(
            self.upload_file_cls.post(**self.mock_kwargs).status_code, 400
        )

    @patch.object(user_ajax, "BlobFileForm")
    def test_form_is_valid_called(self, mock_blob_file_form):
        """test_form_is_valid_called"""
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        self.upload_file_cls.post(**self.mock_kwargs)

        mock_blob_file_form_instance.is_valid.assert_called_once()

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    @patch.object(user_ajax, "blob_api")
    def test_blob_instantiated_for_all_files(
        self, mock_blob_api, mock_blob, mock_blob_file_form
    ):
        """test_blob_instantiated_for_all_files"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        self.upload_file_cls.post(**self.mock_kwargs)

        mock_blob.assert_has_calls(
            [
                call(
                    filename=mock_file.name,
                    blob=mock_file,
                    user_id=str(self.mock_kwargs["request"].user.id),
                )
                for mock_file in mock_file_list
            ]
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    def test_blob_init_exception_returns_http_400(
        self, mock_blob, mock_blob_file_form
    ):
        """test_blob_init_exception_returns_http_400"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance
        mock_blob.side_effect = Exception("mock_blob_exception")

        self.assertEqual(
            self.upload_file_cls.post(**self.mock_kwargs).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    @patch.object(user_ajax, "blob_api")
    def test_blob_inserted_for_all_files(
        self, mock_blob_api, mock_blob, mock_blob_file_form
    ):
        """test_blob_inserted_for_all_files"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        # Ensure that all blob return the MagicMock instance from the file list.
        mock_blob.side_effect = lambda filename, blob, user_id: blob

        self.upload_file_cls.post(**self.mock_kwargs)

        mock_blob_api.insert.assert_has_calls(
            [
                call(item, self.mock_kwargs["request"].user)
                for item in mock_file_list
            ]
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    @patch.object(user_ajax, "blob_api")
    def test_blob_insert_exception_returns_http_400(
        self, mock_blob_api, mock_blob, mock_blob_file_form
    ):
        """test_blob_insert_exception_returns_http_400"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        # Ensure that all blob return the MagicMock instance from the file list.
        mock_blob.side_effect = lambda filename, blob, user_id: blob

        mock_blob_api.insert.side_effect = Exception(
            "mock_blob_insert_exception"
        )

        self.assertEqual(
            self.upload_file_cls.post(**self.mock_kwargs).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    @patch.object(user_ajax, "blob_api")
    def test_success_return_http_200(
        self, mock_blob_api, mock_blob, mock_blob_file_form
    ):
        """test_success_return_http_200"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        # Ensure that all blob return the MagicMock instance from the file list.
        mock_blob.side_effect = lambda filename, blob, user_id: blob

        self.assertEqual(
            self.upload_file_cls.post(**self.mock_kwargs).status_code,
            status.HTTP_200_OK,
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    @patch.object(user_ajax, "blob_api")
    def test_success_return_empty_http_response(
        self, mock_blob_api, mock_blob, mock_blob_file_form
    ):
        """test_success_return_empty_http_response"""
        mock_file_list = [MagicMock(), MagicMock()]
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = True
        mock_blob_file_form_instance.cleaned_data = {"file": mock_file_list}
        mock_blob_file_form.return_value = mock_blob_file_form_instance

        # Ensure that all blob return the MagicMock instance from the file list.
        mock_blob.side_effect = lambda filename, blob, user_id: blob

        self.assertEqual(
            json.loads(self.upload_file_cls.post(**self.mock_kwargs).content),
            {},
        )

    @patch.object(user_ajax, "BlobFileForm")
    @patch.object(user_ajax, "Blob")
    def test_invalid_form_returns_http_400(
        self, mock_blob, mock_blob_file_form
    ):
        """test_invalid_form_returns_http_400"""
        mock_blob_file_form_instance = MagicMock()
        mock_blob_file_form_instance.is_valid.return_value = False

        mock_blob_file_form.return_value = mock_blob_file_form_instance

        self.assertEqual(
            self.upload_file_cls.post(**self.mock_kwargs).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
