""" MongoDB
"""
from mongoengine import connect

from core_main_app.settings import (
    MONGO_USER,
    MONGO_PASS,
    MONGO_HOST,
    MONGO_PORT,
    MONGO_DB,
    MONGODB_INDEXING,
    GRIDFS_STORAGE,
)

MONGODB_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
)

# Connect to MongoDB if indexing or file storage enabled
if MONGODB_INDEXING or GRIDFS_STORAGE:
    MONGO_CLIENT = connect(host=MONGODB_URI, connect=False)
