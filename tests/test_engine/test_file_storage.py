#!/usr/bin/python3
"""
Module of Unittests.
"""
#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
import json

class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

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
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

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
        with open('file.json', 'w') as f:
            pass
        storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

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

    def test_file_path(self):
        """ Confirm __file_path attribute is set """
        self.assertEqual(storage._FileStorage__file_path, "file.json")

    def test_objects_attribute(self):
        """ Confirm __objects attribute is present """
        self.assertTrue(hasattr(storage, "_FileStorage__objects"))
        self.assertIsInstance(storage._FileStorage__objects, dict)

    def test_all_method(self):
        """ Test the all() method """
        new = BaseModel()
        new.save()
        objects = storage.all()
        self.assertIsInstance(objects, dict)
        self.assertIn(new.__class__.__name__ + "." + new.id, objects)

    def test_new_method(self):
        """ Test the new() method """
        new = BaseModel()
        storage.new(new)
        self.assertIn(new.__class__.__name__ + "." + new.id, storage._FileStorage__objects)

    def test_save_method(self):
        """ Test the save() method """
        new = BaseModel()
        storage.new(new)
        storage.save()
        # Check if the file was saved and contains the object
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(new.__class__.__name__ + "." + new.id, data)

    def test_reload_method(self):
        """ Test the reload() method """
        new = BaseModel()
        new.save()
        # Modify the file contents
        with open('file.json', 'w') as f:
            f.write('{"fake_key": "fake_value"}')
        # Perform reload
        storage.reload()
        objects = storage.all()
        # Check if the reloaded objects contain the previous object
        self.assertIn(new.__class__.__name__ + "." + new.id, objects)

if __name__ == '__main__':
    unittest.main()
