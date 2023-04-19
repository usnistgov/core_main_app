""" Integration Test for Data Rest API
"""
from copy import copy
from unittest.mock import patch

from rest_framework import status
from tests.components.data.fixtures.fixtures import (
    DataFixtures,
    QueryDataFixtures,
    AccessControlDataFixture,
)
from tests.components.user.fixtures.fixtures import UserFixtures

from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.models import Workspace
from core_main_app.rest.data import views as data_rest_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    IntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

fixture_data = DataFixtures()
fixture_data_query = QueryDataFixtures()
fixture_data_workspace = AccessControlDataFixture()


class TestDataListByWorkspace(IntegrationBaseTestCase):
    """Test Data List By Workspace"""

    fixture = fixture_data_workspace

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_filtered_by_correct_workspace_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_filtered_by_correct_workspace_returns_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"workspace": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 2)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_filtered_by_incorrect_workspace_returns_no_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_filtered_by_incorrect_workspace_returns_no_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"workspace": -1},
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 0)

    def test_get_all_by_correct_workspace_returns_data(self):
        """test_get_all_by_correct_workspace_returns_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1, is_superuser=True)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataListByWorkspace.as_view(),
            user,
            param={"workspace_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(len(response.data), 2)


class TestDataList(IntegrationBaseTestCase):
    """TestDataList"""

    fixture = fixture_data

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @patch.object(Data, "xml_content")
    def test_get_returns_http_200(
        self, mock_xml_content, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_returns_http_200

        Args:
            get_all_workspaces_with_read_access_by_user
            mock_xml_content:

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), user
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_returns_all_user_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_returns_all_user_data

        Returns:

        """
        # Arrange
        get_all_workspaces_with_read_access_by_user.return_value = []
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(), user
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 2)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_filtered_by_correct_title_returns_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_filtered_by_correct_title_returns_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"title": self.fixture.data_1.title},
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_filtered_by_incorrect_title_returns_no_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_filtered_by_incorrect_title_returns_no_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"title": "bad title"},
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 0)

    def test_get_filtered_by_correct_template_returns_data(self):
        """test_get_filtered_by_correct_template_returns_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"template": self.fixture.data_1.template},
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    def test_get_filtered_by_incorrect_template_returns_no_data(
        self, get_all_workspaces_with_read_access_by_user
    ):
        """test_get_filtered_by_incorrect_template_returns_no_data

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        get_all_workspaces_with_read_access_by_user.return_value = []

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"template": -1},
        )

        # Assert
        self.assertEqual(len(response.data["results"]), 0)

    def test_post_data_missing_field_returns_http_400(self):
        """test_post_data_missing_field_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        mock_data = {
            "template": str(self.fixture.template.id),
            "user_id": "1",
            "xml_content": "<tag></tag>",
        }

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), user, data=mock_data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_data_incorrect_template_returns_http_400(self):
        """test_post_data_incorrect_template_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        mock_data = {
            "template": "507f1f77bcf86cd799439011",
            "user_id": "1",
            "title": "new data",
            "xml_content": "<tag></tag>",
        }

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.DataList.as_view(), user, data=mock_data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDetail(IntegrationBaseTestCase):
    """Test Data Detail"""

    fixture = fixture_data

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    @patch.object(Data, "xml_content")
    def test_get_returns_http_200(self, mock_xml_content):
        """test_get_returns_http_200

        Args:
            mock_xml_content:

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Data, "xml_content")
    def test_get_returns_data(self, mock_xml_content):
        """test_get_returns_data

        Args:
            mock_xml_content:

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        mock_xml_content.return_value = "content"

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.data["title"], self.fixture.data_1.title)

    @patch.object(Data, "xml_content")
    def test_get_data_containing_ascii_returns_data(self, mock_xml_content):
        """test_get_data_containing_ascii_returns_data

        Args:
            mock_xml_content:

        Returns:

        """
        # Arrange
        user = create_mock_user(1)
        mock_xml_content.return_value = "\xc3te\xc3"

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wrong_id_returns_http_404(self):
        """test_delete_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_delete(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_id_returns_http_404(self):
        """test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_template_returns_http_400(self):
        """test_patch_wrong_template_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataDetail.as_view(),
            user,
            data={"template": "507f1f77bcf86cd799439011"},
            param={"pk": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataDownload(IntegrationBaseTestCase):
    """TestDataDownload"""

    fixture = fixture_data

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

    def test_get_returns_http_200(self):
        """test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_wrong_id_returns_http_404(self):
        """test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user(1)

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_with_param_returns_http_200(self):
        """test_get_with_param_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
            data={"pretty_print": "false"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_with_param_returns_http_400_when_content_not_well_formatted(
        self,
    ):
        """test_get_with_param_returns_http_400_when_content_not_well_formatted

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataDownload.as_view(),
            user,
            param={"pk": self.fixture.data_1.id},
            data={"pretty_print": "true"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestExecuteLocalQueryView(IntegrationBaseTestCase):
    """TestExecuteLocalQueryView"""

    fixture = fixture_data_query

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()
        # FIXME: unable to test paginated results (mocked queryset.count always returns 0)
        self.data = {"all": "true"}
        # create user with superuser access to skip access control
        self.user = create_mock_user(1, is_superuser=True)

    def test_post_query_string_one_data_returns_http_200(self):
        """test_post_query_string_one_data_returns_http_200

        Returns:

        """
        # Arrange
        self.data.update({"query": '{"root.element": "value"}'})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_query_string_one_data_returns_one_data(self):
        """test_post_query_string_one_data_returns_one_data

        Returns:

        """
        # Arrange
        self.data.update({"query": '{"root.element": "value"}'})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_string_two_data_returns_two_data(self):
        """test_post_query_string_two_data_returns_two_data

        Returns:

        """
        # Arrange
        self.data.update(
            {
                "query": '{"$or": [{"root.element": "value"}, {"root.element":"value2"}]}'
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_post_empty_query_string_filter_by_templates_returns_all_data_of_the_template(
        self,
    ):
        """test_post_empty_query_string_filter_by_templates_returns_all_data_of_the_template

        Returns:

        """
        # Arrange
        self.data.update(
            {"query": "{}", "templates": [{"id": self.fixture.template.id}]}
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_post_query_string_filtered_by_templates_returns_one_data(self):
        """test_post_query_string_filtered_by_templates_returns_one_data

        Returns:

        """
        # Arrange
        self.data.update(
            {
                "query": '{"root.element": "value"}',
                "templates": [{"id": self.fixture.template.id}],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_string_filtered_by_wrong_template_id_returns_no_data(
        self,
    ):
        """test_post_query_string_filtered_by_wrong_template_id_returns_no_data

        Returns:

        """
        # Arrange
        self.data.update(
            {
                "query": '{"root.element": "value"}',
                "templates": [{"id": -1}],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_query_json_returns_http_200(self):
        """test_post_query_json_returns_http_200

        Returns:

        """
        # Arrange
        self.data.update({"query": {}})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_query_json_int_returns_data_1(self):
        """test_post_query_json_int_returns_data_1

        Returns:

        """
        # Arrange
        self.data.update({"query": {"root.complex.child2": 0}})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_string_returns_data_1(self):
        """test_post_query_json_string_returns_data_1

        Returns:

        """
        # Arrange
        self.data.update({"query": {"root.complex.child1": "test"}})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_regex_returns_all_data(self):
        """test_post_query_json_regex_returns_all_data

        Returns:

        """
        # Arrange
        self.data.update({"query": {"root.element": "/.*/"}})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), len(self.fixture.data_collection))

    def test_post_query_json_or_operator_returns_data_1_and_data_2(self):
        """test_post_query_json_or_operator_returns_data_1_and_data_2

        Returns:

        """
        # Arrange
        self.data.update(
            {
                "query": {
                    "$or": [
                        {"root.element": "value"},
                        {"root.element": "value2"},
                    ]
                }
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), len(self.fixture.data_collection))

    def test_post_query_json_and_operator_returns_data_1(self):
        """test_post_query_json_and_operator_returns_data_1

        Returns:

        """
        # Arrange
        self.data.update(
            {
                "query": {
                    "$and": [
                        {"root.complex.child2": {"$lt": 1}},
                        {"root.complex.child2": {"$gte": 0}},
                    ]
                }
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_query_json_element_match_operator_returns_data_1(self):
        """test_post_query_json_element_match_operator_returns_data_1

        Returns:

        """
        # Arrange
        self.data.update(
            {"query": {"root.list": {"$elemMatch": {"element_list_1": 1}}}}
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)


class TestExecuteLocalQueryViewWorkspaceCase(IntegrationTransactionTestCase):
    """TestExecuteLocalQueryViewWorkspaceCase"""

    fixture = fixture_data_workspace

    def setUp(self):
        """setUp

        Returns:

        """
        super().setUp()

        self.data = {"all": "true"}

        # create user with superuser access to skip access control
        self.user = create_mock_user(1, is_superuser=True)

        self.user2 = UserFixtures().create_user()

        self.user2.id = int(self.fixture.data_4.user_id)

    def test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_superuser(
        self,
    ):
        """test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_superuser

        Returns:

        """

        # Arrange
        self.data.update({"query": "{}", "workspaces": []})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 5)

    def test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_user(
        self,
    ):
        """test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_user

        Returns:

        """

        # Arrange
        self.data.update({"query": "{}", "workspaces": []})
        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user2,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 2)

        for data in response.data:
            self.assertEqual(str(data["user_id"]), str(self.user2.id))

    def test_post_empty_query_string_filter_by_one_workspace_returns_all_data_of_the_workspace(
        self,
    ):
        """test_post_empty_query_string_filter_by_one_workspace_returns_all_data_of_the_workspace

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [{"id": self.fixture.workspace_1.id}],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 2)

        for data in response.data:
            self.assertEqual(
                str(data["workspace"]), str(self.fixture.workspace_1.id)
            )

    def test_post_empty_query_string_filter_by_workspaces_returns_all_data_of_those_workspaces(
        self,
    ):
        """test_post_empty_query_string_filter_by_workspaces_returns_all_data_of_those_workspaces

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [
                    {"id": self.fixture.workspace_1.id},
                    {"id": self.fixture.workspace_2.id},
                ],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 3)

        list_ids = [
            str(self.fixture.workspace_1.id),
            str(self.fixture.workspace_2.id),
        ]
        for data in response.data:
            self.assertIn(str(data["workspace"]), list_ids)

    def test_post_query_filter_by_correct_and_wrong_workspaces_returns_data_from_correct_workspace_only_as_superuser(
        self,
    ):
        """test_post_query_filter_by_correct_and_wrong_workspaces_returns_data_from_correct_workspace_only_as_superuser

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [
                    {"id": -1},
                    {"id": self.fixture.workspace_2.id},
                ],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

        for data in response.data:
            self.assertEqual(
                str(data["workspace"]), str(self.fixture.workspace_2.id)
            )

    def test_post_query_filter_by_correct_and_wrong_workspaces_raises_acl_error(
        self,
    ):
        """test_post_query_filter_by_correct_and_wrong_workspaces_raises_acl_error

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [
                    {"id": str(self.fixture.workspace_1.id)},
                    {"id": str(self.fixture.workspace_2.id)},
                ],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user2,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_post_query_string_filter_by_workspace_returns_data_3(self):
        """test_post_query_string_filter_by_workspace_returns_data_3

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": '{"root.element": "value2"}',
                "workspaces": [{"id": self.fixture.workspace_1.id}],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 1)

        for data in response.data:
            self.assertEqual(str(data["id"]), str(self.fixture.data_3.id))
            self.assertEqual(
                str(data["workspace"]), str(self.fixture.workspace_1.id)
            )

    def test_post_query_string_filter_by_workspace_returns_no_data(self):
        """test_post_query_string_filter_by_workspace_returns_no_data

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": '{"root.element": "value2"}',
                "workspaces": [{"id": str(self.fixture.workspace_2.id)}],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_query_string_filter_by_private_workspace_returns_all_data_with_no_workspace_as_superuser(
        self,
    ):
        """test_post_query_string_filter_by_private_workspace_returns_all_data_with_no_workspace_as_superuser

        Returns:

        """

        # Arrange
        self.data.update({"query": "{}", "workspaces": [{"id": "None"}]})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 2)
        for data in response.data:
            self.assertEqual(data["workspace"], None)

    def test_post_query_string_filter_by_private_workspace_raises_acl_error(
        self,
    ):
        """test_post_query_string_filter_by_private_workspace_raises_acl_error

        Returns:

        """

        # Arrange
        self.data.update({"query": "{}", "workspaces": [{"id": None}]})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user2,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_post_query_filter_by_private_and_normal_workspaces_returns_all_data_of_those_workspaces_as_superuser(
        self,
    ):
        """test_post_query_filter_by_private_and_normal_workspaces_returns_all_data_of_those_workspaces_as_superuser

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [
                    {"id": "None"},
                    {"id": self.fixture.workspace_2.id},
                ],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 3)

        list_ids = ["None", str(self.fixture.workspace_2.id)]
        for data in response.data:
            self.assertIn(str(data["workspace"]), list_ids)

    def test_post_query_filter_by_private_and_normal_workspaces_raises_acl_error(
        self,
    ):
        """test_post_query_filter_by_private_and_normal_workspaces_raises_acl_error

        Returns:

        """

        # Arrange
        self.data.update(
            {
                "query": "{}",
                "workspaces": [
                    {"id": "None"},
                    {"id": self.fixture.workspace_2.id},
                ],
            }
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user2,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, 403)

    def test_post_filtered_by_wrong_workspace_id_returns_no_data(self):
        """test_post_filtered_by_wrong_workspace_id_returns_no_data

        Returns:

        """
        # Arrange
        self.data.update({"query": "{}", "workspaces": [{"id": -1}]})

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(len(response.data), 0)


class TestDataAssign(IntegrationBaseTestCase):
    """TestDataAssign"""

    fixture = fixture_data_workspace

    @patch.object(Workspace, "get_by_id")
    @patch.object(Data, "get_by_id")
    def test_get_returns_http_200(self, data_get_by_id, workspace_get_by_id):
        """test_get_returns_http_200

        Args:
            data_get_by_id:
            workspace_get_by_id:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_1

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            user,
            param={"pk": data.id, "workspace_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    @patch.object(Data, "get_by_id")
    def test_assign_data_to_workspace_updates_workspace(
        self, data_get_by_id, workspace_get_by_id
    ):
        """test_assign_data_to_workspace_updates_workspace

        Args:
            data_get_by_id:
            workspace_get_by_id:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            user,
            param={"pk": data.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(
            str(data.workspace.id), str(self.fixture.workspace_2.id)
        )

    @patch.object(Workspace, "get_by_id")
    @patch.object(Data, "get_by_id")
    def test_assign_data_to_workspace_returns_http_200(
        self, data_get_by_id, workspace_get_by_id
    ):
        """test_assign_data_to_workspace_returns_http_200

        Args:
            data_get_by_id:
            workspace_get_by_id:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            user,
            param={"pk": data.id, "workspace_id": self.fixture.workspace_2.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(Workspace, "get_by_id")
    def test_assign_bad_data_id_returns_http_404(self, workspace_get_by_id):
        """test_assign_bad_data_id_returns_http_404

        Args:
            workspace_get_by_id:

        Returns:

        """
        # Arrange
        fake_data_id = -1
        user = create_mock_user(1, is_superuser=True)
        workspace_get_by_id.return_value = self.fixture.workspace_2

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            user,
            param={
                "pk": fake_data_id,
                "workspace_id": self.fixture.workspace_2.id,
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(Data, "get_by_id")
    def test_assign_bad_workspace_id_returns_http_404(self, data_get_by_id):
        """test_assign_bad_workspace_id_returns_http_404

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        fake_workspace_id = -1
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user = create_mock_user(data.user_id, is_superuser=True)
        data_get_by_id.return_value = data

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataAssign.as_view(),
            user,
            param={"pk": data.id, "workspace_id": fake_workspace_id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDataChangeOwner(IntegrationBaseTestCase):
    """TestDataChangeOwner"""

    fixture = fixture_data_workspace

    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_get_returns_http_200_if_user_is_superuser(
        self, data_get_by_id, user_get_by_id
    ):
        """test_get_returns_http_200_if_user_is_superuser

        Args:
            data_get_by_id:
            user_get_by_id:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user(
            "65467", is_staff=True, is_superuser=True
        )
        user_new_owner = create_mock_user("123")
        data_get_by_id.return_value = data
        user_get_by_id.return_value = user_new_owner

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            user_request,
            param={"pk": data.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_get_returns_http_200_if_user_is_not_superuser_but_have_access_to_the_data(
        self, data_get_by_id, user_get_by_id
    ):
        """test_get_returns_http_200_if_user_is_not_superuser_but_have_access_to_the_data

        Args:
            data_get_by_id:
            user_get_by_id:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user(1, is_staff=True)
        user_new_owner = create_mock_user("123")
        data_get_by_id.return_value = data
        user_get_by_id.return_value = user_new_owner

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            user_request,
            param={"pk": data.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        "core_main_app.components.workspace.api.get_all_workspaces_with_read_access_by_user"
    )
    @patch("core_main_app.components.user.api.get_user_by_id")
    @patch.object(Data, "get_by_id")
    def test_get_returns_http_403_if_user_is_not_superuser_or_have_no_access_to_the_data(
        self, data_get_by_id, user_get_by_id, read_access_mock
    ):
        """test_get_returns_http_403_if_user_is_not_superuser_or_have_no_access_to_the_data

        Args:
            data_get_by_id:
            user_get_by_id:
            read_access_mock:

        Returns:

        """
        # Arrange
        data = self.fixture.data_collection[self.fixture.USER_1_WORKSPACE_1]
        user_request = create_mock_user("65467", is_staff=True)
        user_new_owner = create_mock_user("123")
        data_get_by_id.return_value = data
        user_get_by_id.return_value = user_new_owner
        read_access_mock.return_value = []

        # Act
        response = RequestMock.do_request_patch(
            data_rest_views.DataChangeOwner.as_view(),
            user_request,
            param={"pk": data.id, "user_id": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDataPermissions(IntegrationTransactionTestCase):
    """TestDataPermissions"""

    fixture = fixture_data_workspace

    def setUp(self):
        """Insert needed data.

        Returns:

        """
        super().setUp()
        self.fixture.insert_data()
        self.fixture.generate_workspace_with_perm()
        self.admin_user = UserFixtures().create_super_user("admin")

    def test_get_returns_correct_permissions_if_user_is_superuser(self):
        """test_get_returns_correct_permissions_if_user_is_superuser

        Returns:

        """
        # Arrange
        user_request = create_mock_user(1, is_superuser=True)
        data = self.fixture.data_4

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = True
        self.assertEqual(response.data, excepted_result)

    def test_get_returns_correct_permissions_if_user_is_anonymous(self):
        """test_get_returns_correct_permissions_if_user_is_anonymous

        Returns:

        """
        # Arrange
        user_request = create_mock_user(1, is_anonymous=True)
        data = self.fixture.data_4

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = False
        self.assertEqual(response.data, excepted_result)

    @patch.object(data_api, "get_by_id")
    def test_get_returns_correct_permissions_if_user_is_not_owner(
        self, data_get_by_id
    ):
        """test_get_returns_correct_permissions_if_user_is_not_owner

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        user_request = UserFixtures().create_user(
            "no_owner_user", is_staff=True
        )
        data = self.fixture.data_4
        data_get_by_id.return_value = data

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = False
        self.assertEqual(response.data, excepted_result)

    @patch.object(data_api, "get_by_id")
    def test_get_returns_correct_permissions_if_user_is_owner(
        self, data_get_by_id
    ):
        """test_get_returns_correct_permissions_if_user_is_owner

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        user_request = UserFixtures().create_user("owner_user", is_staff=True)
        data = copy(self.fixture.data_3)  # do not alter the fixture object
        data.user_id = str(user_request.id)
        data.workspace = None
        data_get_by_id.return_value = data

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = True
        self.assertEqual(response.data, excepted_result)

    @patch.object(data_api, "get_by_id")
    def test_get_if_user_has_read_permission_in_workspace(
        self, data_get_by_id
    ):
        """test_get_if_user_has_read_permission_in_workspace

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        user_request = UserFixtures().create_user("read_user")
        data = self.fixture.data_collection[self.fixture.USER_2_WORKSPACE_2]
        data_get_by_id.return_value = data
        workspace_api.add_user_read_access_to_workspace(
            self.fixture.workspace_2, user_request, self.admin_user
        )

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = False
        self.assertEqual(response.data, excepted_result)

    @patch.object(data_api, "get_by_id")
    def test_get_if_user_has_write_permission_in_workspace(
        self, data_get_by_id
    ):
        """test_get_if_user_has_write_permission_in_workspace

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        user_request = UserFixtures().create_user("write_user")
        data = self.fixture.data_collection[self.fixture.USER_2_WORKSPACE_2]
        data_get_by_id.return_value = data
        workspace_api.add_user_write_access_to_workspace(
            self.fixture.workspace_2, user_request, self.admin_user
        )

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = True
        self.assertEqual(response.data, excepted_result)

    @patch.object(data_api, "get_by_id")
    def test_get_if_user_has_write_read_permission_in_workspace(
        self, data_get_by_id
    ):
        """test_get_if_user_has_write_read_permission_in_workspace

        Args:
            data_get_by_id:

        Returns:

        """
        # Arrange
        user_request = UserFixtures().create_user("rw_user")
        data = self.fixture.data_collection[self.fixture.USER_2_WORKSPACE_2]
        data_get_by_id.return_value = data
        workspace_api.add_user_read_access_to_workspace(
            self.fixture.workspace_2, user_request, self.admin_user
        )
        workspace_api.add_user_write_access_to_workspace(
            self.fixture.workspace_2, user_request, self.admin_user
        )

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataPermissions.as_view(),
            user_request,
            data={"ids": f'["{data.id}"]'},
        )

        # Assert
        excepted_result = {}
        excepted_result[str(data.id)] = True
        self.assertEqual(response.data, excepted_result)
