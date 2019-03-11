""" Integration Test for Data Rest API
"""

from mock import patch
from rest_framework import status

from core_main_app.components.data.models import Data
from core_main_app.components.workspace.models import Workspace
from core_main_app.rest.data import views as data_rest_views
from core_main_app.utils.integration_tests.integration_base_test_case import \
    MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.data.fixtures.fixtures import DataFixtures, QueryDataFixtures, AccessControlDataFixture

fixture_data = DataFixtures()
fixture_data_query = QueryDataFixtures()
fixture_data_workspace = AccessControlDataFixture()


class TestDataList(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestDataList, self).setUp()

    @patch.object(Data, 'xml_content')
    def test_get_returns_http_200(self, mock_xml_content):
        # Arrange
        user = create_mock_user('1')
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(), user)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_all_user_data(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(), user)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_correct_title_returns_data(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(),
                                              user,
                                              data={'title': self.fixture.data_1.title})

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_title_returns_no_data(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(),
                                              user,
                                              data={'title': 'bad title'})

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_get_filtered_by_correct_template_returns_data(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(),
                                              user,
                                              data={'template': self.fixture.data_1.template})

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_get_filtered_by_incorrect_template_returns_no_data(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataList.as_view(),
                                              user,
                                              data={'template': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_data_missing_field_returns_http_400(self):
        # Arrange
        user = create_mock_user('1')
        mock_data = {'template': str(self.fixture.template.id),
                     'user_id': '1',
                     'xml_content': '<tag></tag>'}

        # Act
        response = RequestMock.do_request_post(data_rest_views.DataList.as_view(),
                                               user,
                                               data=mock_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_data_incorrect_template_returns_http_400(self):
        # Arrange
        user = create_mock_user('1')
        mock_data = {'template': '507f1f77bcf86cd799439011',
                     'user_id': '1',
                     'title': 'new data',
                     'xml_content': '<tag></tag>'}

        # Act
        response = RequestMock.do_request_post(data_rest_views.DataList.as_view(),
                                               user,
                                               data=mock_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDetail(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestDataDetail, self).setUp()

    @patch.object(Data, 'xml_content')
    def test_get_returns_http_200(self, mock_xml_content):
        # Arrange
        user = create_mock_user('1')
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDetail.as_view(),
                                              user,
                                              param={'pk': self.fixture.data_1.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, 'xml_content')
    def test_get_returns_data(self, mock_xml_content):
        # Arrange
        user = create_mock_user('1')
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDetail.as_view(),
                                              user,
                                              param={'pk': self.fixture.data_1.id})

        # Assert
        self.assertEqual(response.data['title'], self.fixture.data_1.title)

    @patch.object(Data, 'xml_content')
    def test_get_data_containing_ascii_returns_data(self, mock_xml_content):
        # Arrange
        user = create_mock_user('1')
        mock_xml_content.return_value = "\xc3te\xc3"

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDetail.as_view(),
                                              user,
                                              param={'pk': self.fixture.data_1.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDetail.as_view(),
                                              user,
                                              param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_delete(data_rest_views.DataDetail.as_view(),
                                                 user,
                                                 param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataDetail.as_view(),
                                                user,
                                                param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_template_returns_http_400(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataDetail.as_view(),
                                                user,
                                                data={'template': '507f1f77bcf86cd799439011'},
                                                param={'pk': self.fixture.data_1.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDownload(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestDataDownload, self).setUp()

    def test_get_returns_http_200(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDownload.as_view(),
                                              user,
                                              param={'pk': self.fixture.data_1.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user('1')

        # Act
        response = RequestMock.do_request_get(data_rest_views.DataDownload.as_view(),
                                              user,
                                              param={'pk': '507f1f77bcf86cd799439011'})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestExecuteLocalQueryView(MongoIntegrationBaseTestCase):
    fixture = fixture_data_query

    def setUp(self):
        super(TestExecuteLocalQueryView, self).setUp()
        # FIXME: unable to test paginated results (mocked queryset.count always returns 0)
        self.data = {"all": "true"}
        # create user with superuser access to skip access control
        self.user = create_mock_user('1', is_superuser=True)

    def test_post_query_string_one_data_returns_http_200(self):
        # Arrange
        self.data.update({"query": "{\"root.element\": \"value\"}"})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_query_string_one_data_returns_one_data(self):
        # Arrange
        self.data.update({"query": "{\"root.element\": \"value\"}"})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_string_two_data_returns_two_data(self):
        # Arrange
        self.data.update({"query": "{\"$or\": [{\"root.element\": \"value\"}, {\"root.element\":\"value2\"}]}"})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_post_empty_query_string_filter_by_templates_returns_all_data_of_the_template(self):
        # Arrange
        self.data.update({"query": "{}",
                          "templates": '[{"id": "' + str(self.fixture.template.id) + '"}]'})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_post_query_string_filtered_by_templates_returns_one_data(self):
        # Arrange
        self.data.update({"query": "{\"root.element\": \"value\"}",
                          "templates": '[{"id": "' + str(self.fixture.template.id) + '"}]'})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_string_filtered_by_wrong_template_id_returns_no_data(self):
        # Arrange
        self.data.update({"query": "{\"root.element\": \"value\"}",
                          "templates": '[{"id": "507f1f77bcf86cd799439011"}]'})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_query_json_returns_http_200(self):
        # Arrange
        self.data.update({"query": {}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_query_json_int_returns_data_1(self):
        # Arrange
        self.data.update({"query": {"root.complex.child2": 0}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_string_returns_data_1(self):
        # Arrange
        self.data.update({"query": {"root.complex.child1": "test"}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_regex_returns_all_data(self):
        # Arrange
        self.data.update({"query": {"root.element": "/.*/"}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), len(self.fixture.data_collection))

    def test_post_query_json_or_operator_returns_data_1_and_data_2(self):
        # Arrange
        self.data.update({"query": {"$or": [{"root.element": "value"}, {"root.element": "value2"}]}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), len(self.fixture.data_collection))

    def test_post_query_json_and_operator_returns_data_1(self):
        # Arrange
        self.data.update({"query": {"$and": [{"root.complex.child2": {"$lt": 1}}, {"root.complex.child2": { "$gte": 0 }}]}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_element_match_operator_returns_data_1(self):
        # Arrange
        self.data.update({"query": {"root.list": {"$elemMatch": {"element_list_1": 1}}}})

        # Act
        response = RequestMock.do_request_post(data_rest_views.ExecuteLocalQueryView.as_view(),
                                               self.user,
                                               data=self.data)

        # Assert
        self.assertEqual(len(response.data), 1)


class TestDataAssign(MongoIntegrationBaseTestCase):
    fixture = fixture_data_workspace

    @patch.object(Workspace, 'get_by_id')
    @patch.object(Data, 'get_by_id')
    def test_get_returns_http_200(self, data_get_by_id, workspace_get_by_id):
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_1

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataAssign.as_view(),
                                                user,
                                                param={'pk': data.id,
                                                       'workspace_id': self.fixture.workspace_1.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, 'get_by_id')
    @patch.object(Data, 'get_by_id')
    def test_assign_data_to_workspace_updates_workspace(self, data_get_by_id, workspace_get_by_id):
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        RequestMock.do_request_patch(data_rest_views.DataAssign.as_view(),
                                     user,
                                     param={'pk': data.id,
                                            'workspace_id': self.fixture.workspace_2.id})

        # Assert
        self.assertEqual(str(data.workspace.id), str(self.fixture.workspace_2.id))

    @patch.object(Workspace, 'get_by_id')
    @patch.object(Data, 'get_by_id')
    def test_assign_data_to_workspace_returns_http_200(self, data_get_by_id, workspace_get_by_id):
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataAssign.as_view(),
                                                user,
                                                param={'pk': data.id,
                                                       'workspace_id': self.fixture.workspace_2.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, 'get_by_id')
    def test_assign_bad_data_id_returns_http_404(self, workspace_get_by_id):
        # Arrange
        fake_data_id = '507f1f77bcf86cd799439011'
        user = create_mock_user('1', is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataAssign.as_view(),
                                                user,
                                                param={'pk': fake_data_id,
                                                       'workspace_id': self.fixture.workspace_2.id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, 'get_by_id')
    def test_assign_bad_workspace_id_returns_http_404(self, data_get_by_id):
        # Arrange
        fake_workspace_id = '507f1f77bcf86cd799439011'
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data

        # Act
        response = RequestMock.do_request_patch(data_rest_views.DataAssign.as_view(),
                                                user,
                                                param={'pk': data.id,
                                                       'workspace_id': fake_workspace_id})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
