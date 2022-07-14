""" Unit tests of system API
"""
from collections import OrderedDict
from unittest.case import TestCase

from mock import patch

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from core_main_app.system import api as system_api


def _get_template():
    """get template

    Returns:

    """

    template = Template()
    template.pk = 1
    xsd = (
        "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>"
        "<xs:element name='tag'></xs:element></xs:schema>"
    )
    template.content = xsd
    return template


def _get_workspace():
    """get workspace

    Returns:

    """
    workspace = Workspace()
    workspace.title = "title"
    workspace.owner = 1
    workspace.is_public = True
    workspace.pk = 1
    return workspace


class TestSystemGetAllExcept(TestCase):
    """TestSystemGetAllExcept"""

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_return_data_object(self, mock_get_all_except):
        """test system get all except return data object

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_return_correct_count(self, mock_get_all_except):
        """test system get all except return correct count

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_empty_list_return_data_object(
        self, mock_get_all_except
    ):
        """test system get all except empty list return data object

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except([])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_empty_list_return_correct_count(
        self, mock_get_all_except
    ):
        """test system get all except empty list return correct count

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except([])
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_bad_id_return_data_object(self, mock_get_all_except):
        """test system get all except bad id return data object

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_except")
    def test_system_get_all_except_bad_id_return_correct_count(
        self, mock_get_all_except
    ):
        """test system get all except bad id return correct count

        Args:
            mock_get_all_except:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
        )
        mock_get_all_except.return_value = [mock_data]

        result = system_api.get_all_except(["1"])
        self.assertEqual(len(result), 1)


class TestGetAllDataInWorkspaces(TestCase):
    """TestGetAllDataInWorkspaces"""

    @patch.object(Data, "get_all_by_list_workspace")
    def test_returns_data_object(self, mock_get_all_by_list_workspace):
        """test returns data object

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_list_workspace.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces([_get_workspace().pk])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_by_list_workspace")
    def test_returns_correct_count(self, mock_get_all_by_list_workspace):
        """test returns correct count

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_list_workspace.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces([_get_workspace().pk])
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_by_list_workspace")
    def test_none_returns_data_object(self, mock_get_all_by_list_workspace):
        """test none returns data object

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_list_workspace.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces([None])
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_by_list_workspace")
    def test_none_returns_correct_count(self, mock_get_all_by_list_workspace):
        """test none returns correct count

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_list_workspace.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces([None])
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_by_list_workspace")
    def test_empty_list_returns_no_data(self, mock_get_all_by_list_workspace):
        """test empty list returns no data

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_get_all_by_list_workspace.return_value = []

        result = system_api.get_all_data_in_workspaces([])
        self.assertEqual(len(result), 0)

    @patch.object(Data, "get_all_by_list_workspace")
    def test_invalid_workspace_returns_no_data(self, mock_get_all_by_list_workspace):
        """test invalid workspace returns no data

        Args:
            mock_get_all_by_list_workspace:

        Returns:

        """
        mock_get_all_by_list_workspace.return_value = []

        result = system_api.get_all_data_in_workspaces([-1])
        self.assertEqual(len(result), 0)


class TestGetAllDataInWorkspacesForTemplates(TestCase):
    """TestGetAllDataInWorkspacesForTemplates"""

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_returns_data_object(self, mock_get_all_by_templates_and_workspaces):
        """test returns data object

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_templates_and_workspaces.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces_for_templates(
            [_get_workspace().pk], [_get_template().pk]
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_returns_correct_count(self, mock_get_all_by_templates_and_workspaces):
        """test returns correct count

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_templates_and_workspaces.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces_for_templates(
            [_get_workspace().pk], [_get_template().pk]
        )
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_null_workspace_returns_data_object(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test null workspace returns data object

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_templates_and_workspaces.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces_for_templates(
            [None], [_get_template().pk]
        )
        self.assertTrue(all(isinstance(item, Data) for item in result))

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_null_workspace_returns_correct_count(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test null workspace returns correct count

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_data = Data(
            template=_get_template(),
            workspace=_get_workspace(),
            user_id="1",
            dict_content=OrderedDict(),
            title="mock_title",
        )
        mock_get_all_by_templates_and_workspaces.return_value = [mock_data]

        result = system_api.get_all_data_in_workspaces_for_templates(
            [None], [_get_template().pk]
        )
        self.assertEqual(len(result), 1)

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_empty_workspaces_returns_no_data(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test empty workspaces returns no data

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_get_all_by_templates_and_workspaces.return_value = []

        result = system_api.get_all_data_in_workspaces_for_templates(
            [], [_get_template().pk]
        )
        self.assertEqual(len(result), 0)

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_empty_templates_returns_no_data(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test empty templates returns no data

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_get_all_by_templates_and_workspaces.return_value = []

        result = system_api.get_all_data_in_workspaces_for_templates(
            [_get_workspace().pk], []
        )
        self.assertEqual(len(result), 0)

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_invalid_workspace_returns_no_data(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test invalid workspace returns no data

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_get_all_by_templates_and_workspaces.return_value = []

        result = system_api.get_all_data_in_workspaces_for_templates(
            [-1], [_get_template().pk]
        )
        self.assertEqual(len(result), 0)

    @patch.object(Data, "get_all_by_templates_and_workspaces")
    def test_invalid_template_returns_no_data(
        self, mock_get_all_by_templates_and_workspaces
    ):
        """test invalid template returns no data

        Args:
            mock_get_all_by_templates_and_workspaces:

        Returns:

        """
        mock_get_all_by_templates_and_workspaces.return_value = []

        result = system_api.get_all_data_in_workspaces_for_templates(
            [_get_workspace().pk], [-1]
        )
        self.assertEqual(len(result), 0)
