#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import storage
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="delete")

    else:
        @property
        def cities(self):
            """ getter attribute for cities """
            from models.city import City

            objects = storage.all(City)
            return [obj for obj in objects.values() if obj.state_id == self.id]