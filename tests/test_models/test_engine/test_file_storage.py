#!/usr/bin/python3
"""Module for testing  FileStorage class."""
import unittest
import os
import json
from datetime import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """ Reset the FileStorage objects before each test"""
        FileStorage._FileStorage__objects = {}
        # Create an instance of FileStorage
        self.storage = FileStorage()

    def tearDown(self):
        """ Remove the test file if it exists after each test"""
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_all_method(self):
        """ Test the all method returns the correct dictionary"""
        self.assertEqual(self.storage.all(), {})

        # Add some objects to the FileStorage
        obj1 = BaseModel()
        obj2 = User()
        self.storage.new(obj1)
        self.storage.new(obj2)

        """
        Test that all method returns the
        correct dictionary with added objects
        """
        expected_result = {
            f"BaseModel.{obj1.id}": obj1,
            f"User.{obj2.id}": obj2
        }
        self.assertEqual(self.storage.all(), expected_result)

    def test_new_method(self):
        """Test the new method adds an object to the __objects dictionary"""
        obj = BaseModel()
        self.storage.new(obj)
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save_method(self):
        """Test the save method writes to the file and updates __objects"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()

        # Read the file and compare the contents
        with open(FileStorage._FileStorage__file_path, 'r',
                  encoding="utf-8") as file:
            file_content = json.load(file)

        expected_content = {f"BaseModel.{obj.id}": obj.to_dict()}
        self.assertEqual(file_content, expected_content)


if __name__ == '__main__':
    unittest.main()
