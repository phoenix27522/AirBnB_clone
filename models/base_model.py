#!/usr/bim/python3
"""Module for Base class
Contains the Base class for the AirBnB clone console.
"""

from datetime import datetime
import uuid
import models


class BaseModel:
    """Base class for all models in the application.

    Attributes:
        id (str): Identifier for the model instance.
        created_at (datetime): Timestamp indicating when
                               the model instance was created.
        updated_at (datetime): Timestamp indicating when
                               the model instance was last updated.
    """

    def __init__(self, *args, **kwargs):
        """Initialization of a Base instance.

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-value arguments
        """
        if not kwargs or ('id' not in kwargs or 'created_at'
                          not in kwargs or 'updated_at' not in kwargs):
            self.id = str(uuid.uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()
            models.storage.new(self)
        else:
            kwargs.pop('__class__', None)
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)

    def __str__(self):
        """String representation of the class."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        base_dict = self.__dict__.copy()
        base_dict['__class__'] = self.__class__.__name__
        base_dict['created_at'] = base_dict['created_at'].isoformat()
        base_dict['updated_at'] = base_dict['updated_at'].isoformat()
        return base_dict
