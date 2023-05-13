#!/usr/bin/python3
"""
file_storage.py

Stores instance dictionaries into JSON format files.
"""

import json
import os
import sys
from models import *  # import all models


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""

        # if cls is not given, return all objects
        if not cls:
            return self.__objects

        # if cls is a string, return objects of that class
        elif isinstance(cls, str):
            return {key: value for key, value in self.__objects.items()
                    if isinstance(value, eval(cls))}

        # if cls is a class, return objects of that class
        else:
            return {key: value for key, value in self.__objects.items()
                    if isinstance(value, cls)}

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()

        # create directory if it doesn't exist
        if not os.path.exists("data"):
            os.mkdir("data")

        # write objects to file
        with open(os.path.join("data", FileStorage.__file_path), 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objects_dict = json.load(f)
            for key, value in objects_dict.items():
                class_name, obj_id = key.split('.')
                cls = getattr(sys.modules[__name__], class_name)
                self.new(cls(**value))
        except Exception as e:
            pass
