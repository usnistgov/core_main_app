"""Query tool unit tests
"""
import copy
import re
from unittest import TestCase

from django.test import override_settings

from core_main_app.commons.exceptions import QueryError
from core_main_app.utils.query.mongo.prepare import (
    _compile_regex,
    _add_sub_document_root,
    sanitize_number,
    sanitize_value,
    convert_to_django,
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
            isinstance(
                query["$and"][0]["$or"][0]["dot.notation.1"], re.Pattern
            )
        )
        self.assertTrue(
            isinstance(
                query["$and"][0]["$or"][1]["dot.notation.1.#text"], re.Pattern
            )
        )
        self.assertFalse(
            isinstance(
                query["$and"][1]["$or"][0]["dot.notation.2"], re.Pattern
            )
        )
        self.assertFalse(
            isinstance(
                query["$and"][1]["$or"][1]["dot.notation.2"], re.Pattern
            )
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
            "$or": [
                {"dot.notation": {"$gt": 0}},
                {"dot.notation.#text": {"$gt": 0}},
            ]
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
            "$and": [
                {"dot.notation": {"$gt": 0}},
                {"dot.notation.#text": {"$gt": 0}},
            ]
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
            "$or": [
                {"dot.notation": {"$gt": 0}},
                {"dot.notation.#text": {"$gt": 0}},
            ]
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


class TestSanitizeNumber(TestCase):
    """TestSanitizeNumber"""

    def test_sanitize_number_with_int_is_ok(self):
        """test_sanitize_number_with_int_is_ok

        Returns:

        """
        self.assertTrue(isinstance(sanitize_number(3), int))

    def test_sanitize_number_with_int_str_is_raises_error(self):
        """test_sanitize_number_with_int_str_is_raises_error

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_number("3")

    def test_sanitize_number_with_float_is_ok(self):
        """test_sanitize_number_with_float_is_ok

        Returns:

        """
        self.assertTrue(isinstance(sanitize_number(3.0), float))

    def test_sanitize_number_with_float_str_raises_error(self):
        """test_sanitize_number_with_float_str_raises_error

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_number("3.0")

    def test_sanitize_number_with_string_raises_error(self):
        """test_sanitize_number_with_string_raises_error

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_number("test")


class TestSanitizeValue(TestCase):
    """TestSanitizeValue"""

    def test_sanitize_value_with_str_ok(self):
        """test_sanitize_value_with_str_ok

        Returns:

        """
        self.assertIsNotNone(sanitize_value("test"))

    def test_sanitize_value_with_operator_str_raises_error(self):
        """test_sanitize_value_with_str_ok

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_value("$test")

    def test_sanitize_value_with_other_operator_str_raises_error(self):
        """test_sanitize_value_with_str_ok

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_value("te$st")

    def test_sanitize_value_without_operator_in_list_ok(self):
        """test_sanitize_value_with_str_ok

        Returns:

        """
        query_list = ["test1", "test2"]
        self.assertEqual(sanitize_value(query_list), query_list)

    def test_sanitize_value_with_operator_in_list_raises_error(self):
        """test_sanitize_value_with_str_ok

        Returns:

        """
        with self.assertRaises(QueryError):
            sanitize_value(["test", "te$st"])


class TestPrepareQuery(TestCase):
    def test_prepare_text_query_for_postgresql(self):
        """test_prepare_text_query_for_postgresql

        Returns:

        """
        from django.db.models import Q

        expected_query = Q(vector_column="test")
        self.assertEqual(
            convert_to_django({"$text": {"$search": "test"}}), expected_query
        )

    @override_settings(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        }
    )
    def test_prepare_text_query_for_non_postgresql(self):
        """test_prepare_text_query_for_non_postgresql

        Returns:

        """
        from django.db.models import Q

        expected_query = Q(dict_content__icontains="test")
        self.assertEqual(
            convert_to_django({"$text": {"$search": "test"}}), expected_query
        )

    @override_settings(MONGODB_INDEXING=True)
    def test_prepare_text_query_for_mongodb(self):
        """test_prepare_text_query_for_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import Q

        expected_query = Q(**{"__raw__": {"$text": {"$search": "test"}}})
        self.assertEqual(
            convert_to_django({"$text": {"$search": "test"}}), expected_query
        )
