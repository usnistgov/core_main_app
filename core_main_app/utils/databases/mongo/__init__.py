""" MongoDB
"""
from core_main_app.settings import (
    MONGODB_INDEXING,
    GRIDFS_STORAGE,
)

# Connect to MongoDB if indexing or file storage enabled
if MONGODB_INDEXING or GRIDFS_STORAGE:
    from mongoengine import connect

    from core_main_app.settings import (
        MONGO_USER,
        MONGO_PASS,
        MONGO_HOST,
        MONGO_PORT,
        MONGO_DB,
    )

    MONGODB_URI = (
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    )

    MONGO_CLIENT = connect(host=MONGODB_URI, connect=False)
