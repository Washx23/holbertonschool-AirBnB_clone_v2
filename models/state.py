#!/usr/bin/python3
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from os import getenv
# from models.city import City


class State(BaseModel, Base):
    """State class for storing state information"""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", cascade="all, delete", backref="state")
    else:
        @property
        def cities(self):
            from models import storage
            from models.city import City
            cities = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
