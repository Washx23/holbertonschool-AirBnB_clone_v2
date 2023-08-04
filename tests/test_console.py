#!/usr/bin/python3
"""
    Tests for the HBNB console
"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
import os
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """ Tests for the HBNB console """

    @classmethod
    def setUpClass(cls):
        """ Create a console object for each test """
        cls.hbnb = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """ Delete console object at the end """
        del cls.hbnb

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "Test only valid for FileStorage")
    def test_updatedCreate(self):
        with patch("sys.stdout", new=StringIO()) as mock_output:
            self.hbnb.onecmd('create User name="Julian" '
                             'last_name age=8 lat=37.12')
            _id = mock_output.getvalue().strip()

        storage.reload()

        for key, value in storage.all().items():
            self.assertEqual(key, "User." + _id)
            self.assertTrue(getattr(value, 'created_at', None))
            self.assertTrue(getattr(value, 'updated_at', None))
            self.assertEqual(getattr(value, 'name', None), 'Julian')
            self.assertEqual(getattr(value, 'age', None), 8)
            self.assertEqual(getattr(value, 'lat', None), 37.12)
            self.assertTrue('last_name' not in value.__dict__)
