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
        created_at (datetime): Timestamp indicating when the model instance was created.
        updated_at (datetime): Timestamp indicating when the model instance was last updated.
    """

    def __init__(self, id=None, created_at=None, updated_at=None):
        """Initialize a BaseModel instance.

        Args:
            id (int): Identifier for the model instance.
            created_at (datetime, optional): Timestamp indicating when the model instance was created.
                                             Defaults to the current time if not provided.
            updated_at (datetime, optional): Timestamp indicating when the model instance was last updated.
                                             Defaults to the current time if not provided.
        """

        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def __str__(self):
         """Base class defining common attributes/methods for other classes."""

         return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""

        self.updated_at = datetime.now()


    def to_dict(self):
        """Return a dictionary representation of the instance."""
        base_dict = self.__dict__.copy()
        base_dict['__class__'] = self.__class__.__name__  # Ensure '__class__' is in quotes
        base_dict['created_at'] = base_dict['created_at'].isoformat()
        base_dict['updated_at'] = base_dict['updated_at'].isoformat()
        return base_dict
