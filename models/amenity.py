#!/usr/bin/python3
"""Defines Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Repersent Amenity in system

    Attributes:
        name(str): The name of the amenity
    """
    name = ""
