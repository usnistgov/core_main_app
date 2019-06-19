"""Mongo query builder tools
"""
import copy
import re


def _compile_regex(query):
    """Compile all regular expressions in the query

    Args:
        query:

    Returns:

    """
    for key, value in query.items():
        if key == "$and" or key == "$or":
            for sub_value in value:
                _compile_regex(sub_value)
        elif isinstance(value, str) or isinstance(value, str):
            if len(value) >= 2 and value[0] == "/" and value[-1] == "/":
                query[key] = re.compile(value[1:-1])
        elif isinstance(value, dict):
            _compile_regex(value)


def _add_sub_document_root(query, sub_document_root):
    """Adds a sub document root to each criteria

    Returns:

    """
    for key in list(query.keys()):
        if key == "$and" or key == "$or":
            for value in query[key]:
                _add_sub_document_root(value, sub_document_root)
        elif not key.startswith("$"):
            query["{}.{}".format(sub_document_root, key)] = query.pop(key)


def prepare_query(query_dict, regex=True, sub_document_root=None):
    """Prepares the query to before executing it

    Args:
        query_dict:
        regex:
        sub_document_root:

    Returns:

    """
    # get a copy of the query
    query = copy.deepcopy(query_dict)

    if regex:
        # compile the regular expressions
        _compile_regex(query)

    if sub_document_root is not None:
        # add a sub document root
        _add_sub_document_root(query, sub_document_root)

    return query
