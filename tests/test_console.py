#!/usr/bin/python3
"""testing module for the hbnb command console"""

from console import HBNBCommand
from models.engine.file_storage import FileStorage
import unittest
import datetime
from unittest.mock import patch
from io import StringIO
import re
import os
import json
import sys


class TestHBNBCommand(unittest.TestCase):

    """Tests fot the console."""

    def setUp(self):
        """Sets up the test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def tearDown(self):
        pass

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    def resetStorage(self):
        """Resets the FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help(self):
        """Test for the  the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_do_EOF(self):
        """Test for EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    def test_emptyline(self):
        """Test for  emptyl ine functionality."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")
        s = ""
        self.assertEqual(s, f.getvalue())

    def test_do_create(self):
        """Tests create for all classes."""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def test_do_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_do_create(self, classname):
        """Helper method to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))
        self.assertTrue(uid in f.getvalue())

    def test_do_show(self):
        """Tests show for all classes."""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helps test the show command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(uid in s)

    def help_test_show_advanced(self, classname):
        """Helps test .show() command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_show_error(self):
        """Tests show command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_destroy(self):
        """Tests destroy for all classes."""
        for classname in self.classes():
            self.help_test_do_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_do_destroy_error(self):
        """Tests destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_destroy_advanced(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_all(self):
        """Tests all for all classes."""
        for classname in self.classes():
            self.help_test_do_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_do_all(self, classname):
        """Helps test the all command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_do_all_error(self):
        """Tests all command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the .all() command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.all()".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_do_all_error_advanced(self):
        """Tests all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.all()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_count_all(self):
        """Tests count for all classes."""
        for classname in self.classes():
            self.help_test_count_advanced(classname)

    def help_test_count_advanced(self, classname):
        """Helps test .count() command."""
        for i in range(20):
            uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.count()".format(classname))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertEqual(s, "20")

    def test_update_1(self):
        """Tests update 1..."""
        classname = "BaseModel"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_2(self):
        """Tests update 1..."""
        classname = "User"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_3(self):
        """Tests update 1..."""
        classname = "City"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_4(self):
        """Tests update 1..."""
        classname = "State"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_6(self):
        """Tests update 1..."""
        classname = "Amenity"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        cmd = cmd.format(classname, uid, attr, val)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_7(self):
        """Tests update 1..."""
        classname = "Review"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        cmd = cmd.format(classname, uid, attr, val)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_8(self):
        """Tests update 1..."""
        classname = "Place"
        attr = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        cmd = cmd.format(classname, uid, attr, val)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_update_all(self):
        """Tests update command with errthang, like a baws."""
        for classname, cls in self.classes().items():
            uid = self.create_class(classname)
            for attr, value in self.test_random_attributes.items():
                if type(value) is not str:
                    pass
                quotes = (type(value) == str)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, False)
                self.help_test_update(classname, uid, attr,
                                      value, quotes, True)
            pass
            if classname == "BaseModel":
                continue
            for attr, attr_type in self.attributes()[classname].items():
                if attr_type not in (str, int, float):
                    continue
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      True, False)
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      False, True)

    def test_do_update_error(self):
        """Tests update command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6534276893")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {}'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {} name'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def help_load_dict(self, rep):
        """Helper method to test dictionary equality."""
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(rep)
        self.assertIsNotNone(res)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        return d

    def test_do_update_error_advanced(self):
        """Tests update() command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(6534276893)")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(uid))
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def help_test_update(self, classname, uid, attr, val, quotes, func):
        """Tests update commmand."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        uid = self.create_class(classname)
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update("{}", "{}", {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, attr, value_str)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        msg = f.getvalue()[:-1]
        self.assertEqual(len(msg), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(str(val), s)
        self.assertIn(attr, s)

    def test_do_count_error(self):
        """Tests .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.count()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".count()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str}
        }
        return attributes

    def create_class(self, classname):
        """Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes


if __name__ == "__main__":
    unittest.main()