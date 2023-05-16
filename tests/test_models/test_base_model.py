#!/usr/bin/python3
""" Module of Unittests """
import unittest
from models.base_model import BaseModel
import os
import json
from models import storage
from models.engine.file_storage import FileStorage
import datetime


class TestBaseModel(unittest.TestCase):
    """ Suite of Console Tests """

    my_model = BaseModel()

    def test_BaseModel1(self):
        """ Test attributes value of a BaseModel instance """

        self.my_model.name = "Holberton"
        self.my_model.my_number = 89
        self.my_model.save()
        my_model_json = self.my_model.to_dict()

        self.assertEqual(self.my_model.name, my_model_json['name'])
        self.assertEqual(self.my_model.my_number, my_model_json['my_number'])
        self.assertEqual('BaseModel', my_model_json['__class__'])
        self.assertEqual(self.my_model.id, my_model_json['id'])

    def test_save(self):
        """ Testing save metthod"""
        i = BaseModel()
        i.save()
        key = "BaseModel" + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ testing the str method of themodel"""
        i = BaseModel()
        self.assertEqual(str(i), '[{}] ({}) {}'.format("BaseModel", i.id,
                                                       i.__dict__))


if __name__ == '__main__':
    unittest.main()
