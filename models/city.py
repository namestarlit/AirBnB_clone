#!/usr/bin/python3
"""
city.py

Module contains a City class.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """Represents a City class."""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of City."""
        super().__init__(*args, **kwargs)
