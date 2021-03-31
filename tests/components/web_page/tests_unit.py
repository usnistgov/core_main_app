""" Tests of the web page API
"""

from unittest.case import TestCase

from mock import Mock, patch

from core_main_app.commons.enums import WEB_PAGE_TYPES
from core_main_app.commons.exceptions import ApiError
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.web_page import api as web_page_api
from core_main_app.components.web_page.models import WebPage


class TestsWebPageApiGet(TestCase):
    @patch("core_main_app.components.web_page.models.WebPage.get_by_type")
    def test_web_page_get_login(self, mock_get_web_page_by_type):
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
    def test_web_page_get_not_in_database_return_none(self, mock_get_web_page_by_type):
        # Arrange
        mock_get_web_page_by_type.side_effect = DoesNotExist
        # Act
        result = web_page_api.get("fake_type")
        # Assert
        self.assertEqual(None, result)

    def test_web_page_get_with_wrong_type_return_none(self):
        # Arrange
        # Act
        page = web_page_api.get("wrong_type")
        # Assert
        self.assertEqual(None, page)


class TestsWebPageApiUpsert(TestCase):
    def test_web_page_upsert_type_does_not_exist(self):
        # Arrange
        web_page = WebPage(type=4, content="test")
        # Act # Assert
        with self.assertRaises(ApiError):
            web_page_api.upsert(web_page)

    @patch("core_main_app.components.web_page.models.WebPage.save")
    def test_web_page_upsert_type_exist(self, mock_save):
        # Arrange
        web_page_type = WEB_PAGE_TYPES["login"]
        content = "content"
        web_page = WebPage(type=web_page_type, content=content)
        mock_save.return_value = WebPage(type=web_page_type, content=content)
        # Act
        result = web_page_api.upsert(web_page)
        # Assert
        self.assertEquals(content, result.content)


def _create_mock_web_page(page_type=-1, content="content"):
    mock_web_page = Mock(spec=WebPage)
    mock_web_page.type = page_type
    mock_web_page.content = content
    return mock_web_page
