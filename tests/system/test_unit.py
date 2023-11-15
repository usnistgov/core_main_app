""" Unit tests of system API
"""
from collections import OrderedDict
from unittest.case import TestCase
from unittest.mock import patch

from tests.components.data.tests_unit import _get_json_template, _get_template

from core_main_app.commons.exceptions import CoreError
from core_main_app.components.data.models import Data
from core_main_app.components.workspace.models import Workspace
from core_main_app.system import api as system_api


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


class TestSystemUpsert(TestCase):
    """TestSystemUpsert"""

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch.object(Data, "convert_and_save")
    def test_system_upsert_xml_data(
        self,
        mock_convert_and_save,
        mock_check_xml_file_is_valid,
        mock_check_json_file_is_valid,
    ):
        """test_system_upsert_xml_data

        Args:
            mock_convert_and_save:

        Returns:

        """
        # Arrange
        mock_convert_and_save.return_value = None
        mock_check_xml_file_is_valid.return_value = None
        mock_check_json_file_is_valid.return_value = None
        mock_data = Data(
            template=_get_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
            content="<tag></tag>",
        )
        # Act
        system_api.upsert_data(mock_data)
        # Assert
        self.assertTrue(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch.object(Data, "convert_and_save")
    def test_system_upsert_json_data(
        self,
        mock_convert_and_save,
        mock_check_xml_file_is_valid,
        mock_check_json_file_is_valid,
    ):
        """test_system_upsert_json_data

        Args:
            mock_convert_and_save:

        Returns:

        """
        # Arrange
        mock_convert_and_save.return_value = None
        mock_check_xml_file_is_valid.return_value = None
        mock_check_json_file_is_valid.return_value = None
        mock_data = Data(
            template=_get_json_template(),
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
            content="{}",
        )

        # Act
        system_api.upsert_data(mock_data)
        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertTrue(mock_check_json_file_is_valid.called)

    @patch("core_main_app.components.data.api.check_json_file_is_valid")
    @patch("core_main_app.components.data.api.check_xml_file_is_valid")
    @patch.object(Data, "convert_and_save")
    def test_system_upsert_data_with_bad_template(
        self,
        mock_convert_and_save,
        mock_check_xml_file_is_valid,
        mock_check_json_file_is_valid,
    ):
        """test_system_upsert_json_data

        Args:
            mock_convert_and_save:

        Returns:

        """
        # Arrange
        mock_convert_and_save.return_value = None
        mock_check_xml_file_is_valid.return_value = None
        mock_check_json_file_is_valid.return_value = None

        bad_format_template = _get_template()
        bad_format_template.format = "bad"
        mock_data = Data(
            template=bad_format_template,
            user_id="1",
            dict_content=OrderedDict(),
            title="title",
            content="{}",
        )

        # Act + Assert
        with self.assertRaises(CoreError):
            system_api.upsert_data(mock_data)

        # Assert
        self.assertFalse(mock_check_xml_file_is_valid.called)
        self.assertFalse(mock_check_json_file_is_valid.called)
