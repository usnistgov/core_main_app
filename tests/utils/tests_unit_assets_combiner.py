""" Assets Combiner utils test class
"""

from unittest import TestCase

from core_main_app.utils.assets_combiner import join_assets


class TestJoinAssets(TestCase):
    """Test to_bool"""

    def test_join_assets_empty_returns_empty_dict(self):
        """test_join_assets_empty_returns_empty_dict

        Returns:

        """

        self.assertEqual(join_assets(), {})

    def test_join_one_assets_returns_assets(self):
        """test_join_assets_returns_assets

        Returns:

        """
        assets = {
            "js": [
                {"path": "file_1", "is_raw": False},
                {"path": "file_2", "is_raw": False},
                {"path": "file_3", "is_raw": False},
            ],
            "css": ["test.css"],
        }
        self.assertEqual(join_assets(assets), assets)

    def test_join_assets_returns_assets(self):
        """test_join_assets_returns_assets

        Returns:

        """
        assets_1 = {
            "js": [
                {"path": "file_1", "is_raw": False},
                {"path": "file_2", "is_raw": False},
            ]
        }
        assets_2 = {
            "js": [
                {"path": "file_3", "is_raw": False},
                {"path": "file_4", "is_raw": False},
            ],
            "css": ["test.css"],
        }

        assets_3 = {
            "other_key": ["test"],
        }

        expected_result = {
            "js": [
                {"path": "file_1", "is_raw": False},
                {"path": "file_2", "is_raw": False},
                {"path": "file_3", "is_raw": False},
                {"path": "file_4", "is_raw": False},
            ],
            "css": ["test.css"],
            "other_key": ["test"],
        }

        self.assertEqual(
            join_assets(assets_1, assets_2, assets_3), expected_result
        )
