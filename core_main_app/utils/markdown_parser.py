""" Parser to convert Markdown to HTML in a safe way
"""
from markdown import markdown

from xml_utils.commons.exceptions import HTMLError
from xml_utils.html_tree.parser import safe_html


def parse(text):
    """Parse Markdown to convert it into HTML

    Args:
        text:

    Returns:
    """
    md_text = markdown(text)

    try:
        return safe_html(md_text)
    except HTMLError as exception:
        return str(exception)
