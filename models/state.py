#!/usr/bin/python3
"""class that difines state"""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents the state of the user in the system
    Attributes :
        name(str): name of the state
    """
    name = ""
