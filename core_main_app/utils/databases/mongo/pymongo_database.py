"""
    The Database pymongo tool contains the available function relative to database operation (connection)
"""
import logging
import re

logger = logging.getLogger(__name__)


def get_full_text_query(text):
    """Return a full text query.

    Args:
        text: List of keywords

    Returns: The corresponding query

    """
    full_text_query = {}
    word_list = re.sub(r"[^\w]", " ", text, flags=re.UNICODE).split()
    word_list = ['"' + x + '"' for x in word_list]
    word_list = " ".join(word_list)
    if len(word_list) > 0:
        full_text_query = {"$text": {"$search": word_list}}

    return full_text_query


def init_text_index(document_object):
    """Create index for full text search."""
    collection = document_object._get_collection()
    collection.create_index(
        [("$**", "text")], default_language="en", language_override="en"
    )
