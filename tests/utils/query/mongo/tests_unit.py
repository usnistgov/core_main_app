"""Query tool unit tests
"""
import copy
import re
from unittest import TestCase

from core_main_app.utils.query.mongo.prepare import (
    _compile_regex,
    _add_sub_document_root,
)


class TestCompileRegex(TestCase):
    """TestCompileRegex"""

    def test_query_with_regex_returns_query_with_compiled_regex(self):
        """test query with regex returns query with compiled regex

        Returns:

        """
        # set query
        query = {"dot.notation": "/regex/"}
        # compile regex
        _compile_regex(query)
        # assert
        self.assertTrue(isinstance(query["dot.notation"], re.Pattern))

    def test_query_with_regex_on_multiple_levels_returns_query_with_compiled_regex(
        self,
    ):
        """test query with regex on multiple levels returns query with compiled regex

        Returns:

        """
        # set query
        query = {
            "$and": [
                {
                    "$or": [
                        {"dot.notation.1": "/regex/"},
                        {"dot.notation.1.#text": "/regex/"},
                    ]
                },
                {
                    "$or": [
                        {"dot.notation.2": {"$lt": 500}},
                        {"dot.notation.2": {"$lt": 500}},
                    ]
                },
            ]
        }
        # compile regex
        _compile_regex(query)
        # assert
        self.assertTrue(
            isinstance(query["$and"][0]["$or"][0]["dot.notation.1"], re.Pattern)
        )
        self.assertTrue(
            isinstance(query["$and"][0]["$or"][1]["dot.notation.1.#text"], re.Pattern)
        )
        self.assertFalse(
            isinstance(query["$and"][1]["$or"][0]["dot.notation.2"], re.Pattern)
        )
        self.assertFalse(
            isinstance(query["$and"][1]["$or"][1]["dot.notation.2"], re.Pattern)
        )

    def test_query_without_regex_returns_same_query(self):
        """test query without regex returns same query

        Returns:

        """
        # set query
        query = {"dot.notation": {"$gt": 0}}
        # save original query
        query_origin = copy.deepcopy(query)
        # compile regex
        _compile_regex(query)
        # assert
        self.assertEqual(query, query_origin)

    def test_query_without_regex_on_multiple_levels_returns_same_query(self):
        """test query without regex on multiple levels returns same query

        Returns:

        """
        # set query
        query = {
            "$or": [{"dot.notation": {"$gt": 0}}, {"dot.notation.#text": {"$gt": 0}}]
        }
        # save original query
        query_origin = copy.deepcopy(query)
        # compile regex
        _compile_regex(query)
        # assert
        self.assertEqual(query, query_origin)


class TestAddSubDocumentRoot(TestCase):
    """TestAddSubDocumentRoot"""

    def test_add_sub_document_root_to_query(self):
        """test add sub document root to query

        Returns:

        """
        # set query
        query = {"dot.notation": "test"}
        # set expected query
        expected_query = {"root.dot.notation": "test"}
        # compile regex
        _add_sub_document_root(query, "root")
        # assert
        self.assertEqual(query, expected_query)

    def test_add_sub_document_root_to_and_query(self):
        """test add sub document root to and query

        Returns:

        """
        # set query
        query = {
            "$and": [{"dot.notation": {"$gt": 0}}, {"dot.notation.#text": {"$gt": 0}}]
        }
        # set expected query
        expected_query = {
            "$and": [
                {"root.dot.notation": {"$gt": 0}},
                {"root.dot.notation.#text": {"$gt": 0}},
            ]
        }
        # compile regex
        _add_sub_document_root(query, "root")
        # assert
        self.assertEqual(query, expected_query)

    def test_add_sub_document_root_to_or_query(self):
        """test add sub document root to or query

        Returns:

        """
        # set query
        query = {
            "$or": [{"dot.notation": {"$gt": 0}}, {"dot.notation.#text": {"$gt": 0}}]
        }
        # set expected query
        expected_query = {
            "$or": [
                {"root.dot.notation": {"$gt": 0}},
                {"root.dot.notation.#text": {"$gt": 0}},
            ]
        }
        # compile regex
        _add_sub_document_root(query, "root")
        # assert
        self.assertEqual(query, expected_query)

    def test_add_sub_document_root_to_and_or_query(self):
        """test add sub document root to and or query

        Returns:

        """
        # set query
        query = {
            "$and": [
                {
                    "$or": [
                        {"dot.notation.1": "test"},
                        {"dot.notation.1.#text": "/regex/"},
                    ]
                },
                {
                    "$or": [
                        {"dot.notation.2": {"$lt": 500}},
                        {"dot.notation.2": {"$lt": 500}},
                    ]
                },
            ]
        }
        # set expected query
        expected_query = {
            "$and": [
                {
                    "$or": [
                        {"root.dot.notation.1": "test"},
                        {"root.dot.notation.1.#text": "/regex/"},
                    ]
                },
                {
                    "$or": [
                        {"root.dot.notation.2": {"$lt": 500}},
                        {"root.dot.notation.2": {"$lt": 500}},
                    ]
                },
            ]
        }
        # compile regex
        _add_sub_document_root(query, "root")
        # assert
        self.assertEqual(query, expected_query)
