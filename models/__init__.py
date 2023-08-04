#!/usr/bin/python3
"""
    This module instantiates the storage object to persist
    objects (either to a file or a database)
"""
from os import getenv

storageType = getenv("HBNB_TYPE_STORAGE")

if storageType == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
