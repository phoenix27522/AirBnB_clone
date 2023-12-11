#!/usr/bin/python3
"""Unittest module for the User Class."""

import unittest
import os
from datetime import datetime
from models.user import User
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """test cases for user"""

    def setUp(self):
        """ set up tests"""
        self.user = User()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_user_inherits_from_base_model(self):
        """ test inheritance"""
        self.assertIsInstance(self.user, BaseModel)

    def test_user_attributes(self):
        """ test user attributes"""
        self.assertTrue(hasattr(self.user, 'email'))
        self.assertTrue(hasattr(self.user, 'password'))
        self.assertTrue(hasattr(self.user, 'first_name'))
        self.assertTrue(hasattr(self.user, 'last_name'))

    def test_user_attributes_default_values(self):
        """ test default values for user attributes """
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_attributes_assignment(self):
        """ test user attr  assignment """
        self.user.email = "test@example.com"
        self.user.password = "securepassword"
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.password, "securepassword")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
    """
    def test_user_to_dict_method(self):
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertIn('id', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)
        self.assertIn('email', user_dict)
        self.assertIn('password', user_dict)
        self.assertIn('first_name', user_dict)
        self.assertIn('last_name', user_dict)
    """

    def test_user_str_representation(self):
        """ test str representation """
        self.assertEqual(str(self.user), "[User] ({}) {}"
                         .format(self.user.id, self.user.__dict__))


if __name__ == '__main__':
    unittest.main()
