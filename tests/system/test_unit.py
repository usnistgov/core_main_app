""" Unit tests of system API
"""
from collections import OrderedDict
from unittest.case import TestCase
from unittest.mock import patch

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
    def test_system_get_all_except_return_data_object(
        self, mock_get_all_except
    ):
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
    def test_system_get_all_except_return_correct_count(
        self, mock_get_all_except
    ):
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
    def test_system_get_all_except_bad_id_return_data_object(
        self, mock_get_all_except
    ):
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
