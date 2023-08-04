#!/usr/bin/python3
"""Unittest for DBStorage"""
import unittest
from models import storage
from models.user import User
from os import getenv


class TestDBStorage(unittest.TestCase):
    """Defines the TestDBStorage class"""

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'only testing db storage')
    def test_all(self):
        """Test the all() method"""
        user = User(email="test@test.com", password="testpass")
        user.save()
        objs = storage.all(User)
        self.assertIn(user, objs.values())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'only testing db storage')
    def test_new(self):
        """Test the new() method"""
        user = User(email="test@test.com", password="testpass")
        storage.new(user)
        objs = storage.all(User)
        self.assertIn(user, objs.values())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'only testing db storage')
    def test_save(self):
        """Test the save() method"""
        user = User(email="test@test.com", password="testpass")
        storage.new(user)
        storage.save()
        objs = storage.all(User)
        self.assertIn(user, objs.values())

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', 'only testing db storage')
    def test_delete(self):
        """Test the delete() method"""
        user = User(email="test@test.com", password="testpass")
        storage.new(user)
        storage.save()
        storage.delete(user)
        objs = storage.all(User)
        self.assertNotIn(user, objs.values())
