""" List of available uri resolvers for lxml
"""
from core_main_app.utils.resolvers.requests_resolver import RequestsResolver

XSD_URI_RESOLVERS = {
    "REQUESTS_RESOLVER": RequestsResolver,
}
