#!/usr/bin/python3
""" Tests for the DBStorage class """
import unittest
import os
import MySQLdb
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """ Tests for the DBStorage class """

    @classmethod
    def setUpClass(cls):
        """
            Set the environ variables for storage to test functionality
            of the program with SQLAlchemy
        """
        envVariables = {"HBNB_MYSQL_USER": "hbnb_test",
                        "HBNB_MYSQL_PWD": "hbnb_test_pwd",
                        "HBNB_MYSQL_HOST": "localhost",
                        "HBNB_MYSQL_DB": "hbnb_test_db",
                        "HBNB_ENV": "test"}

        os.environ.update(envVariables)

    def setUp(self):
        """ Set up the connection to the database and the cursor """
        self.conn = MySQLdb.connect(host="localhost",
                                    user="hbnb_test",
                                    passwd="hbnb_test_pwd",
                                    db="hbnb_test_db")
        self.cursor = self.conn.cursor()

        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """ Close the connection to the db and the cursor """
        self.cursor.close()
        self.conn.close()
        self.storage.close()

    @classmethod
    def tearDownClass(cls):
        """ Remove the created environment variables """
        envVariables = {"HBNB_MYSQL_USER": "hbnb_test",
                        "HBNB_MYSQL_PWD": "hbnb_test_pwd",
                        "HBNB_MYSQL_HOST": "localhost",
                        "HBNB_MYSQL_DB": "hbnb_test_db",
                        "HBNB_ENV": "test"}

        for key in envVariables:
            del os.environ[key]

    def test_createAndSave(self):
        """ Test that an object is corretcly created in the db """
        from models.state import State
        from models.city import City
        new_state = State(name="Florida")
        new_city = City(name="Miami", state_id=new_state.id)
        self.storage.new(new_state)
        self.storage.save()
        self.storage.new(new_city)
        self.storage.save()

        self.cursor.execute("SELECT name FROM states")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], new_state.name)

        self.cursor.execute("SELECT name FROM cities")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], new_city.name)

    def test_deleteAndSave(self):
        """ Test that delete method works correcly on DB """
        from models.state import State
        NY = State(name="New York")
        CA = State(name="California")
        self.storage.new(NY)
        self.storage.new(CA)
        self.storage.save()

        self.cursor.execute("SELECT name FROM states")
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 2)

        self.storage.delete(NY)
        self.storage.delete(CA)
        self.storage.save()

        # for whatever reason MySQLdb doesn't track the deletion
        # unless we close and reopen the connection to the db.
        self.cursor.close()
        self.conn.close()

        self.conn = MySQLdb.connect(host="localhost",
                                    user="hbnb_test",
                                    passwd="hbnb_test_pwd",
                                    db="hbnb_test_db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT name FROM states")
        result = self.cursor.fetchall()
        self.assertEqual(len(result), 0)

    def test_reload(self):
        """
            Test that objects persist in the database even if
            we close and reopen the session / delete the storage var
        """
        from models.state import State
        self.storage.new(State(name="Florida"))
        self.storage.save()
        self.storage.close()
        self.storage.reload()

        self.cursor.execute("SELECT name FROM states")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "Florida")
