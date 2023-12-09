#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """class that stores info and help to serialize and desrialize.

    Attributes:
        __file_path(str): the name of the file to the objects to.
        __objects(dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """sets a unique identifier "id" """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serialize the __object to json file. """
        ob_dict = FileStorage.__objects
        new_dict = {j: ob_dict[j].to_dict() for j in ob_dict.keys()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(new_dict, file)

    def reload(self):
        """Deserialize the json file """
        try:
            with open(FileStorage.__file_path) as file:
                new_dict = json.load(file)
                for i in new_dict.values():
                    name_cls = i["__class__"]
                    del i["__class__"]
                    self.new(eval(name_cls)(**i))
        except FileNotFoundError:
            return
