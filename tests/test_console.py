#!/usr/bin/python3
""" unittest for the console """
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class TestConsole(unittest.TestCase):
    """ Test for the console """
    def setUp(self):
        """ Setup """
        self.cli = HBNBCommand()

    def tearDown(self):
        """ Teardown """
        self.cli = None

    def test_create(self):
        self.cli.onecmd("create State name='California'")
        output = self.cli.output
        state_id = output.strip().split()[-1][:-1]
        self.assertTrue(len(state_id) == 36)
        self.cli.onecmd("show State {}".format(state_id))
        output = self.cli.output
        self.assertTrue("California" in output)

    def test_create(self):
        """ Test create """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create State name='California'")
            output = f.getvalue().strip()
            self.assertTrue(output.startswith(""))

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(
                "create Place city_id='0001' user_id='0001'\
                    name='House' number_rooms=3 number_bathrooms=2\
                        max_guest=6 price_by_night=150")
            output = f.getvalue().strip()
            self.assertTrue(output.startswith(""))

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create Amenity name='Kitchen'")
            output = f.getvalue().strip()
            self.assertTrue(output.startswith(""))

    def test_show(self):
        """ Test show """
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show State")
            self.assertEqual("** instance id missing **\n", f.getvalue())

        state = State(name="California")
        storage.new(state)
        storage.save()

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show State {}".format(state.id))
            output = f.getvalue().strip()
            self.assertTrue(output.startswith("[State]"))

    def test_destroy(self):
        """ test destroy """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 1234-1234-1234")
            self.assertEqual("** no instance found **\n", f.getvalue())


if __name__ == '__main__':
    unittest.main()
