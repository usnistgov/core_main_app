"""Parser util for text editor
"""


def get_parser(request=None):
    """Load configuration for the parser.

    Args:
        request:

    Returns:

    """
    from core_parser_app.tools.parser.parser import XSDParser

    return XSDParser(
        min_tree=True,
        ignore_modules=True,
        collapse=True,
        auto_key_keyref=False,
        implicit_extension_base=False,
        download_dependencies=False,
        request=request,
    )
