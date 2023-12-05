#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
import models

class FileStorage:
    """class that stores info and helps to serialize and deserialize.

    Attributes:
        _file_path(str): the name of the file to store the objects.
        _objects(dict): A dictionary of instantiated objects.
    """

    _file_path = "airbnb.json"
    _objects = {}

    def all(self):
        """Returns the dictionary of _objects."""
        return self._objects

    def new(self, obj):
        """Sets a unique identifier "id"."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self._objects[key] = obj

    def save(self):
        """Serializes the _objects to a JSON file."""
        new_dict = {key: obj.to_dict() for key, obj in self._objects.items()}
        with open(self._file_path, "w") as file:
            json.dump(new_dict, file)

    def reload(self):
        """Deserializes the JSON file."""
        try:
            with open(self._file_path) as file:
                new_dict = json.load(file)
                for i in new_dict.values():
                    name_cls = i.pop("__class__", None)
                    if name_cls:
                        cls = getattr(models, name_cls, None)
                        if cls:
                            self.new(cls(**i))
                    else:
                        raise ValueError("Missing '__class__' key in JSON")
        except FileNotFoundError:
            # Handle the case where the file is not found
            pass
