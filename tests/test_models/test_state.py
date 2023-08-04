#!/usr/bin/python3
""" """
import unittest
from models.state import State
from models.engine.db_storage import DBStorage
from tests.test_models.test_base_model import test_basemodel
from sqlalchemy import inspect, String, Integer, DateTime
from models import storage


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    """ @unittest.skipUnless(type(storage) is DBStorage,
                         "Test only valid for DBStorage")
    def test_name3(self):
        """ """
        new = self.value()
        inspector = inspect(_DBStorage.__engine)
        column = inspector.get_columns('states', 'name')[0]
        self.assertEqual(column['type'], String(128)) """

    def test_cities(self):
        """ test cities getter """
        from models.city import City
        Fl = State(name="Florida")
        NY = State(name="New York")
        Tx = State(name="Texas")
        storage.new(Fl)
        storage.new(NY)
        storage.new(Tx)
        storage.save()

        Miami = City(name="Miami", state_id=Fl.id)
        NYC = City(name="New Yok City", state_id=NY.id)
        Austin = City(name="Austin", state_id=Tx.id)
        TXC = City(name="Texas City", state_id=Tx.id)
        storage.new(Miami)
        storage.new(NYC)
        storage.new(Austin)
        storage.new(TXC)
        storage.save()

        self.assertEqual(len(Fl.cities), 1)
        self.assertEqual(len(NY.cities), 1)
        self.assertEqual(len(Tx.cities), 2)
