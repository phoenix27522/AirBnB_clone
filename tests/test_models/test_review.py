#!/usr/bin/python3
"""Unittest module for the Review Class."""

import unittest
import os
from datetime import datetime
from models.review import Review
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    def setUp(self):
        self.review = Review()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_review_inherits_from_base_model(self):
        self.assertIsInstance(self.review, BaseModel)

    def test_review_attributes(self):
        self.assertTrue(hasattr(self.review, 'place_id'))
        self.assertTrue(hasattr(self.review, 'user_id'))
        self.assertTrue(hasattr(self.review, 'text'))

    def test_review_attributes_default_values(self):
        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_review_attributes_assignment(self):
        self.review.place_id = "123"
        self.review.user_id = "456"
        self.review.text = "A great place!"
        self.assertEqual(self.review.place_id, "123")
        self.assertEqual(self.review.user_id, "456")
        self.assertEqual(self.review.text, "A great place!")

    """
    def test_review_to_dict_method(self):
        review_dict = self.review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertIn('id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)
        self.assertIn('place_id', review_dict)
        self.assertIn('user_id', review_dict)
        self.assertIn('text', review_dict)
    """
    def test_review_str_representation(self):
        self.assertEqual(str(self.review), "[Review] ({}) {}"
                         .format(self.review.id, self.review.__dict__))


if __name__ == '__main__':
    unittest.main()
