""" Integration Test for Blob Rest API
"""
import unittest
from os.path import join, dirname, abspath

from django.test import override_settings
from rest_framework import status

from core_main_app.components.blob import api as blob_api
from core_main_app.rest.blob import views
from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.blob.fixtures.fixtures import BlobFixtures

RESOURCES_PATH = join(dirname(abspath(__file__)), 'data')
fixture_blob = BlobFixtures()


class TestBlobList(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobList, self).setUp()
        self.data = {'filename': 'file.txt',
                     'blob': open(join(RESOURCES_PATH, 'test.txt'), 'r')}

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_all_user_blobs(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user)

        # Assert
        self.assertEqual(len(response.data), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_as_superuser_returns_all_user_blobs(self):
        # Arrange
        user = create_mock_user('1', is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user)

        # Assert
        self.assertEqual(len(response.data), 3)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_correct_name_returns_http_200(self):
        # Arrange
        user = create_mock_user('1', is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user,
                                              data={'filename': self.fixture.blob_1.filename})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_correct_name_returns_correct_blob(self):
        # Arrange
        user = create_mock_user('1', is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user,
                                              data={'filename': self.fixture.blob_1.filename})

        # Assert
        self.assertEqual(response.data[0]['filename'], self.fixture.blob_1.filename)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_incorrect_name_returns_http_200(self):
        # Arrange
        user = create_mock_user('1', is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user,
                                              data={'filename': 'incorrect'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_filtered_by_incorrect_name_returns_empty_list(self):
        # Arrange
        user = create_mock_user('1', is_superuser=True)

        # Act
        response = RequestMock.do_request_get(views.BlobList.as_view(),
                                              user,
                                              data={'filename': 'incorrect'})

        # Assert
        self.assertEqual(len(response.data), 0)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_returns_http_201(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_post(views.BlobList.as_view(),
                                               user,
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_adds_an_entry_in_database(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_post(views.BlobList.as_view(),
                                               user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(blob_api.get_all()), 4)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_post_incorrect_file_parameter_returns_http_400(self):
        # Arrange
        user = create_mock_user('1')
        self.data['blob'] = 'test.txt'

        # Act
        response = RequestMock.do_request_post(views.BlobList.as_view(),
                                               user,
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBlobDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDetail, self).setUp()

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobDetail.as_view(),
                                              user,
                                              param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_blob(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobDetail.as_view(),
                                              user,
                                              param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.data['filename'], self.fixture.blob_1.filename)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobDetail.as_view(),
                                              user,
                                              param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_200(self):
        # Arrange
        user = create_mock_user('2')

        # Act
        response = RequestMock.do_request_get(views.BlobDetail.as_view(),
                                              user,
                                              param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_returns_http_204(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_delete(views.BlobDetail.as_view(),
                                                 user,
                                                 param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_deletes_one_blob_from_database(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_delete(views.BlobDetail.as_view(),
                                                 user,
                                                 param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(len(blob_api.get_all()), 2)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_delete(views.BlobDetail.as_view(),
                                                 user,
                                                 param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_blob_returns_http_403(self):
        # Arrange
        user = create_mock_user('2')

        # Act
        response = RequestMock.do_request_delete(views.BlobDetail.as_view(),
                                                 user,
                                                 param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_delete_other_user_as_superuser_returns_http_204(self):
        # Arrange
        user = create_mock_user('2', is_superuser=True)

        # Act
        response = RequestMock.do_request_delete(views.BlobDetail.as_view(),
                                                 user,
                                                 param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestBlobDownload(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDownload, self).setUp()
        self.blob = open(join(RESOURCES_PATH, 'test.txt'), 'r').read()

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobDownload.as_view(),
                                              user,
                                              param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(views.BlobDownload.as_view(),
                                              user,
                                              param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @unittest.skip("need to mock GridFS Blob Host")
    @override_settings(ROOT_URLCONF="core_main_app.urls")
    def test_get_other_user_blob_returns_http_200(self):
        # Arrange
        user = create_mock_user('2')

        # Act
        response = RequestMock.do_request_get(views.BlobDownload.as_view(),
                                              user,
                                              param={'pk': str(self.fixture.blob_1.id)})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestBlobDeleteList(MongoIntegrationBaseTestCase):
    fixture = fixture_blob

    def setUp(self):
        super(TestBlobDeleteList, self).setUp()
        self.data = [{'id': str(self.fixture.blob_1.id)},
                     {'id': str(self.fixture.blob_2.id)}]

    def test_post_a_list_containing_other_user_blob_returns_http_403(self):
        # Arrange
        user = create_mock_user('2')

        # Act
        response = RequestMock.do_request_patch(views.BlobDeleteList.as_view(),
                                                user,
                                                data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip("need to mock GridFS Blob Host")
    def test_post_a_list_containing_other_user_blob_as_superuser_returns_http_204(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_patch(views.BlobDeleteList.as_view(),
                                                user,
                                                data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
