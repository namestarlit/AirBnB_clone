#!/usr/bin/python3
"""
user.py

Module contains User class.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """Represents a User class."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
