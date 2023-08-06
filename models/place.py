#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv

place_amenity_association = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60),
           ForeignKey("places.id"), nullable=False),
    Column('amenity_id', String(60),
           ForeignKey("amenities.id"), nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship("Amenity",
                                 secondary=place_amenity_association,
                                 viewonly=False,
                                 back_populates="place_amenities")

    else:
        @property
        def reviews(self):
            """ Getter method for reviews """
            from models.review import Review

            objects = storage.all(Review)
            return [obj for obj in objects.values() if obj.place_id == obj.id]

        @property
        def amenities(self):
            """ Getter method for amenities """
            return amenity_ids

        @amenities.setter
        def amenities(self, obj):
            """ Add an object to the amenities present in a place """
            from models.amenity import Amenity

            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenities_ids.append(obj.id)