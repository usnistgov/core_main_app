""" MongoDB test settings
"""
from tests.test_settings import *
from core_main_app.utils.databases.mongo.mongoengine_database import Database

MONGODB_INDEXING = True
MONGODB_ASYNC_SAVE = False

MOCK_DATABASE_NAME = "db_mock"
MOCK_DATABASE_HOST = "mongomock://localhost"

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()