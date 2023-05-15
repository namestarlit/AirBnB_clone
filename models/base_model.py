#!/usr/bin/python3
"""
base_model.py

A base module that contains the base model class.
"""

from uuid import uuid4
from datetime import datetime
import models


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

        # Update instance attributes with kwargs.
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """String Representation of BaseModel class."""
        return "[{:s}] ({:s}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute 'updated_at'."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary of all the key/value of the '__dict__'."""
        # Create a new dict from instance '__dict__'
        new_dict = self.__dict__.copy()

        # Convert 'created_at' and 'updated_at' into ISO format.
        new_dict['__class__'] = self.__class__.__name__

        for key, value in self.__dict__.items():
            if key == 'created_at' or key == 'updated_at':
                new_dict[key] = value.isoformat()

        return new_dict
