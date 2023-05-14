#!/usr/bin/python3
"""
console.py

A console application for Airbnb clone.
"""

import cmd
import sys
import re
import os

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city  import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBConsole(cmd.Cmd):
    """Represents HBNBConsole class."""

    # Define console  prompt
    if sys.__stdin__.isatty():
        prompt = "(hbnb) "
    else:
        prompt = ""

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True
    def postloop(self):
        print()


if __name__ == "__main__":
    HBNBConsole().cmdloop()
