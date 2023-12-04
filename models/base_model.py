#!/usr/bim/python3
"""Module for Base class
Contains the Base class for the AirBnB clone console.
"""

from datetime import datetime
import uuid


class BaseModel:
    """Base class for all models in the application.

    Attributes:
        id (int): Identifier for the model instance.
        created_at (datetime): Timestamp indicating when
                               the model instance was created.
        updated_at (datetime): Timestamp indicating when the
                               model instance was last updated.
    """

    def __init__(self, *args, **kwargs):
        """Initialization of a Base instance.

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """
        if kwargs is not None and kwargs != {}:
            kwargs.pop('__class__', None)
            for key, value in kwargs.items():
                if key == "created_at":
                    setattr(self, "created_at", datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key == "updated_at":
                    setattr(self, "updated_at", datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = id or str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """string representation of the calss"""

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""

        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary representation of the instance."""

        base_dict = self.__dict__.copy()
        base_dict['__class__'] = self.__class__.__name__
        base_dict['created_at'] = base_dict['created_at'].isoformat()
        base_dict['updated_at'] = base_dict['updated_at'].isoformat()
        return base_dict
