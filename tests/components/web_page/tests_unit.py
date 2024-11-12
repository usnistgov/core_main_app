""" Tests of the web page API
"""

from unittest.case import TestCase
from unittest.mock import Mock, patch

from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.commons.exceptions import ApiError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.web_page import api as web_page_api
from core_main_app.components.web_page.models import WebPage


class TestsWebPageApiGet(TestCase):
    """TestsWebPageApiGet"""

    @patch("core_main_app.components.web_page.models.WebPage.get_by_type")
    def test_web_page_get_login(self, mock_get_web_page_by_type):
        """test web page get login

        Args:
            mock_get_web_page_by_type:

        Returns:

        """
        # Arrange
        content = "content web page login"
        mock_get_web_page_by_type.return_value = _create_mock_web_page(
            WEB_PAGE_TYPES["login"], content
        )
        # Act
        result = web_page_api.get("login")
        # Assert
        self.assertEqual("content web page login", result.content)

    @patch("core_main_app.components.web_page.models.WebPage.get_by_type")
    def test_web_page_get_not_in_database_return_none(
        self, mock_get_web_page_by_type
    ):
        """test web page get not in database return none

        Args:
            mock_get_web_page_by_type:

        Returns:

        """
        # Arrange
        mock_get_web_page_by_type.side_effect = DoesNotExist("")
        # Act
        result = web_page_api.get("login")
        # Assert
        self.assertEqual(None, result)

    def test_web_page_get_with_wrong_type_return_none(self):
        """test web page get with wrong type return none

        Returns:

        """
        # Act
        page = web_page_api.get("wrong_type")
        # Assert
        self.assertEqual(None, page)


class TestsWebPageApiDeleteByType(TestCase):
    """Tests Web Page Api Delete By Type"""

    @patch("core_main_app.components.web_page.models.WebPage.delete_by_type")
    def test_web_page_delete_by_type_raises_error_when_does_not_exist(
        self, mock_delete_by_type
    ):
        """test web page delete by type raises error when does not exist

        Returns:

        """
        # Arrange
        mock_delete_by_type.side_effect = DoesNotExist("")
        # Act # Assert
        with self.assertRaises(DoesNotExist):
            web_page_api.delete_by_type(-1)

    @patch("core_main_app.components.web_page.models.WebPage.delete_by_type")
    def test_web_page_delete_by_type_deletes_web_page(
        self, mock_delete_by_type
    ):
        """test web page delete by type deletes web page

        Args:
            mock_delete_by_type:

        Returns:

        """
        # Arrange
        mock_delete_by_type.return_value = None
        # Act
        result = web_page_api.delete_by_type(1)
        # Assert
        self.assertEqual(result, None)


class TestsWebPageApiUpsert(TestCase):
    """TestsWebPageApiUpsert"""

    def test_web_page_upsert_type_does_not_exist(self):
        """test web page upsert type does not exist

        Returns:

        """
        # Arrange
        web_page = WebPage(type=1000, content="test")
        # Act # Assert
        with self.assertRaises(ApiError):
            web_page_api.upsert(web_page)

    @patch("core_main_app.components.web_page.models.WebPage.save")
    def test_web_page_upsert_type_exist(self, mock_save):
        """test web page upsert type exist

        Args:
            mock_save:

        Returns:

        """
        # Arrange
        web_page_type = WEB_PAGE_TYPES["login"]
        content = "content"
        web_page = WebPage(type=web_page_type, content=content)
        mock_save.return_value = WebPage(type=web_page_type, content=content)
        # Act
        result = web_page_api.upsert(web_page)
        # Assert
        self.assertEqual(content, result.content)

    @patch("core_main_app.components.web_page.models.WebPage.delete_by_type")
    def test_web_page_upsert_type_deletes_when_content_is_empty(
        self, mock_delete_by_type
    ):
        """test web page upsert type deletes when content is empty

        Args:
            mock_delete_by_type:

        Returns:

        """
        # Arrange
        web_page_type = WEB_PAGE_TYPES["login"]
        content = ""
        web_page = WebPage(type=web_page_type, content=content)
        mock_delete_by_type.return_value = None
        # Act
        result = web_page_api.upsert(web_page)
        # Assert
        self.assertEqual(result, None)


def _create_mock_web_page(page_type=-1, content="content"):
    """create mock web page

    Args:
        page_type:
        content:

    Returns:

    """
    mock_web_page = Mock(spec=WebPage)
    mock_web_page.type = page_type
    mock_web_page.content = content
    return mock_web_page
