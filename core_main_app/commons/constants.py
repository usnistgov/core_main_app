""" Constants
"""

MARKDOWN_UNSAFE = 0
MARKDOWN_GENERATION_FAILED = 1

MARKDOWN_ERRORS = [
    "Unprotected script tags have been detected. Please remove them to be able to save your work!",
    "HTML is not generated properly, please check your Markdown and HTML syntax!",
]

UNKNOWN_ERROR = "An unknown error occurred, please contact your administrator for more information."

DATA_JSON_FIELD = "dict_content"

DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT = {"JSON": ".json", "XSD": ".xml"}

DATA_FORMAT_FOR_TEMPLATE_FORMAT = {"JSON": "JSON", "XSD": "XML"}

DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT = {
    "JSON": "application/json",
    "XSD": "text/xml",
}

TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT = {
    "JSON": ".json",
    "XSD": ".xsd",
}

TEMPLATE_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT = {
    "JSON": "application/json",
    "XSD": "text/xml",
}

AVAILABLE_BOOTSTRAP_VERSIONS = ["4.6.2", "5.1.3", "5.3.1"]
