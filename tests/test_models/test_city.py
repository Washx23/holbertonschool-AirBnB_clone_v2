#!/usr/bin/python3
""" """
import unittest
from tests.test_models.test_base_model import test_basemodel
from sqlalchemy import inspect, String, Integer, DateTime
from models import storage
from models.engine.db_storage import DBStorage
from models.city import City


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    """ @unittest.skipUnless(type(storage) is DBStorage,
                         "Test only valid for DBStorage")
    def test_state_id(self):
        """ """
        new = self.value()
        inspector = inspect(storage._DBStorage__engine)
        column = inspector.get_columns('cities', 'state_id')[0]
        self.assertEqual(column['type'], String(60))

    @unittest.skipUnless(type(storage) is DBStorage,
                         "Test only valid for DBStorage")
    def test_name(self):
        """ """
        new = self.value()
        inspector = inspect(storage._DBStorage__engine)
        column = inspector.get_columns('cities', 'name')[0]
        self.assertEqual(column['type'], String(128)) """
