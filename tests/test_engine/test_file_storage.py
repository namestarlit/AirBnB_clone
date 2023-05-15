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

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

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
        storage = FileStorage()
        self.assertEqual(len(storage.all()), 0)

        # Create an object
        obj = BaseModel()
        obj.name = "Test Object"
        obj.save()

        # Verify if the object exists in the __objects dictionary
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, storage.all())

        # Get the dictionary representation of the object
        var1 = obj.to_dict()

        # Create a new key using the object's class name and id
        new_key = "{}.{}".format(var1['__class__'], var1['id'])

        # Save the objects to the file
        storage.save()

        # Load the objects from the file
        with open(os.path.join("data", "file.json"), 'r') as f:
            var2 = json.load(f)

        # Get the object using the new key
        new = var2[new_key]

        # Compare the attributes of the original and loaded objects
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

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        file_path = os.path.join('data', 'file.json')
        self.assertTrue(os.path.exists(file_path))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        file_path = os.path.join('data', 'file.json')
        self.assertNotEqual(os.path.getsize(file_path), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        file_path = os.path.join('data', 'file.json')
        self.assertTrue(os.path.exists(file_path))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        new.save()
        storage.reload()
        loaded = None
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open(os.path.join("data", 'file.json'), 'w') as f:
            pass
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists(os.path.join('data', 'file.json')))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        new.save()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)


if __name__ == '__main__':
    unittest.main()
