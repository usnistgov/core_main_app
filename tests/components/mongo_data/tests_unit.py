""" Unit test for MongoData
"""
import json
from unittest import TestCase
from unittest.mock import patch

from django.test import tag
from tests.components.data.tests_unit import (
    _create_data,
    _create_blob,
    _get_template,
    _get_json_template,
)

from core_main_app.commons.exceptions import ModelError
from core_main_app.components.data.models import Data


class TestMongoDataBlob(TestCase):
    @tag("mongodb")
    @patch.object(Data, "get_by_id")
    def test_data__blob_returns_blob_if_exists(self, mock_get_by_id):
        """

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        blob = _create_blob(user_id="2")
        blob.save()
        template = _get_template()
        template.save()
        data = _create_data(
            data_id=1,
            template=template,
            user_id="2",
            title="new_title",
            content="<tag></tag>",
            blob=blob,
        )
        data.save()
        mock_get_by_id.return_value = data
        mongo_data = MongoData()
        self.assertEqual(mongo_data._blob, blob)

    @tag("mongodb")
    @patch.object(Data, "get_by_id")
    def test_data__blob_returns_none_if_error(self, mock_get_by_id):
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        mock_get_by_id.side_effect = ModelError("error")
        mongo_data = MongoData()
        self.assertIsNone(mongo_data._blob)


class TestMongoDataContent(TestCase):
    @tag("mongodb")
    def test_data_content_returns_content_if_set(self):
        """test_data_content_returns_content_if_set

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data_content = "<tag></tag>"
        mongo_data = MongoData()
        mongo_data._content = data_content

        self.assertEqual(mongo_data.content, data_content)

    @tag("mongodb")
    @patch.object(Data, "get_by_id")
    def test_data_content_returns_data_content_if_not_set(
        self, mock_get_by_id
    ):
        """test_data_content_returns_data_content_if_not_set

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        template = _get_template()
        template.save()
        data_content = "<tag></tag>"
        data = _create_data(
            data_id=1,
            template=template,
            user_id="2",
            title="title",
            content=data_content,
        )
        data.save()
        mock_get_by_id.return_value = data
        mongo_data = MongoData()

        self.assertEqual(mongo_data.content, data_content)

    @tag("mongodb")
    def test_data_content_sets_content(self):
        """test_data_content_sets_content

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data_content = "<tag></tag>"
        mongo_data = MongoData()
        mongo_data.content = data_content

        self.assertEqual(mongo_data._content, data_content)

    @tag("mongodb")
    def test_data_xml_content_returns_content(self):
        """test_data_xml_content_returns_content

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data_content = "<tag></tag>"
        mongo_data = MongoData()
        mongo_data.content = data_content

        self.assertEqual(mongo_data.xml_content, data_content)

    @tag("mongodb")
    def test_data_xml_content_sets_content(self):
        """test_data_xml_content_sets_content

        Returns:

        """
        from core_main_app.components.mongo.models import (
            MongoData,
        )

        data_content = "<tag></tag>"
        mongo_data = MongoData()
        mongo_data.xml_content = data_content

        self.assertEqual(mongo_data._content, data_content)


class TestInitMongoData(TestCase):
    @tag("mongodb")
    @patch("core_main_app.utils.xml.raw_xml_to_dict")
    def test_init_mongo_with_xml_content_converts_content_to_dict(
        self,
        mock_raw_xml_to_dict,
    ):
        """test_init_mongo_with_xml_content

        Returns:

        """
        # Arrange
        template = _get_template()
        template.save()
        data_content = "<tag></tag>"
        data = _create_data(
            data_id=1,
            template=template,
            user_id="2",
            title="title",
            content=data_content,
        )
        mock_raw_xml_to_dict.return_value = {}

        # Act
        data.save()

        # Assert
        self.assertTrue(mock_raw_xml_to_dict.called)

    @tag("mongodb")
    @patch("core_main_app.utils.xml.raw_xml_to_dict")
    def test_init_mongo_with_json_content_sets_dict(
        self,
        mock_raw_xml_to_dict,
    ):
        """test_init_mongo_with_json_content_sets_dict

        Returns:

        """
        # Arrange
        template = _get_json_template()
        template.save()
        data_content = json.dumps({"value": "test"})
        data = _create_data(
            data_id=1,
            template=template,
            user_id="2",
            title="title",
            content=data_content,
        )
        # Act
        data.save()

        # Assert
        self.assertFalse(mock_raw_xml_to_dict.called)
