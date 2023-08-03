#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(
        String(60), primary_key=True, unique=True, nullable=False
        )
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
        )
    updated_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
        )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary with all the keys and values of the instance"""
        from models import storage
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        for key, value in dictionary.items():
            if isinstance(value, datetime):
                dictionary[key] = value.isoformat()
        if '_sa_instance_state' in dictionary:
            dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)
