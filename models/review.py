#!/usr/bin/python3
"""
review.py

Module containing a Review class.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a Review class."""
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of Review."""
        super().__init__(*args, **kwargs)
