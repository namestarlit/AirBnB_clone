#!/usr/bin/python3
"""
state.py

Module contains a State class.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """Represents State class."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of State."""
        super().__init__(*args, **kwargs)
