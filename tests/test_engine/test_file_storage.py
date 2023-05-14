#!/usr/bin/python3
"""
Module of Unittests.
"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
from models.engine.file_storage import FileStorage
from models import storage
import os
import json


class TestFileStorage(unittest.TestCase):
    """ Suite of File Storage Tests """

    my_model = BaseModel()

    def test_instance(self):
        """ Check instance """
        self.assertIsInstance(storage, FileStorage)

    def test_StoreBaseModel(self):
        """ Test save and reload functions """
        self.my_model.full_name = "BaseModel Instance"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        key = bm_dict['__class__'] + "." + bm_dict['id']
        self.assertEqual(key in all_objs, True)

    def test_StoreBaseModel2(self):
        """ Test save, reload and update functions """
        self.my_model.my_name = "First name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        key = bm_dict['__class__'] + "." + bm_dict['id']

        self.assertEqual(key in all_objs, True)
        self.assertEqual(bm_dict['my_name'], "First name")

        create1 = bm_dict['created_at']
        update1 = bm_dict['updated_at']

        self.my_model.my_name = "Second name"
        self.my_model.save()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        self.assertEqual(key in all_objs, True)

        create2 = bm_dict['created_at']
        update2 = bm_dict['updated_at']

        self.assertEqual(create1, create2)
        self.assertNotEqual(update1, update2)
        self.assertEqual(bm_dict['my_name'], "Second name")

    def test_save_Self(self):
        """ Check save self """
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 100)

    def test_save_FileStorage(self):
        """ Test if 'new' method is working good """
        var1 = self.my_model.to_dict()
        new_key = var1['__class__'] + "." + var1['id']
        storage.save()
        with open(os.path.join("data","file.json"), 'r') as f:
            var2 = json.load(f)
        new = var2[new_key]
        for key in new:
            self.assertEqual(var1[key], new[key])

    def test_save(self):
        """ Testing save metthod"""
        i = BaseModel()
        i.save()
        key = "BaseModel" + "." + i.id
        with open(os.path.join('data', 'file.json'), 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ testing the str method of themodel"""
        i = BaseModel()
        self.assertEqual(str(i), '[{}] ({}) {}'.format("BaseModel", i.id,
                         i.__dict__))
    def test_default(self):
        """ default testing of basemodel"""
        i = BaseModel()
        self.assertEqual(type(i), BaseModel)

    def test_kwargs(self):
        """ testing basemodel with kwargs"""
        i = BaseModel()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)


    def test_kwargs_none(self):
        """ testing kwargs again with none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = BaseModel(**n)

    def test_kwargs_one(self):
        """ testing kwargs with one arg"""
        n = {'name': 'test'}
        new = BaseModel(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """ testing id attr of the model"""
        new = BaseModel()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ testing created at attr"""
        new = BaseModel()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ testing updated at attr"""
        new = BaseModel()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

if __name__ == '__main__':
    unittest.main()
