#!/usr/bin/python3
"""Module for City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """Class representing a City in the system."""
    state_id = ""
    name = ""
