""" Unit test for MongoData
"""
from unittest import TestCase
from unittest.mock import patch

from django.test import tag
from tests.components.data.tests_unit import (
    _create_data,
    _create_blob,
    _get_template,
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
