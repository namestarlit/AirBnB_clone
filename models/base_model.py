#!/usr/bin/python3
"""
base_model.py

A base module that contains the base model class.
"""

from uuid import uuid4
from datetime import datetime


class BaseModel(object):
    """Base model class of the clone application."""

    def __init__(self, *args, **kwargs):
        """Initilizes instances of BaseModel class.

        Args:
            *args (tuple): Non-keyworded parameters.
            **kwargs (dict): Keyworded parameters
        """
        # Set Random unique ID to instance attribute 'id'
        self.id = str(uuid4())

        # Set 'created_at' and 'updated_at' attributes.
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Update instance attributes with kwargs.
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" and isinstance(value, str):
                    setattr(self, key, datetime.fromisoformat(value))
                if key == "updated_at" and isinstance(value, str):
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """String Representation of BaseModel class."""
        return "[{:s}] ({:s}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute 'updated_at'."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary of all the key/value of the '__dict__'."""
        # Create a new dict from instance '__dict__'
        new_dict = dict(self.__dict__)

        # Convert 'created_at' and 'updated_at' into ISO format.
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()

        # Set and delete the '__class__' key in the dictionary.
        new_dict['__class__'] = self.__class__.__name__
        del new_dict['__class__']

        return new_dict
