#!/usr/bin/python3
"""
    This module creates the class for the Database Storage System
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    """ DB Storage class for preserving our objects """
    __engine = None
    __session = None

    def __init__(self):
        dialect, driver = 'mysql', 'mysqldb'
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f"{dialect}+{driver}://{user}:{password}"
                                      f"@{host}/{db}",
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
            Query on the current database session
            all objects depending of the class name
        """
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        dictionary = {}
        if cls:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = type(obj).__name__ + '.' + obj.id
                dictionary[key] = obj

        else:
            classes = [State, City, User, Place, Review, Amenity]
            for queryClass in classes:
                qryResult = self.__session.query(queryClass).all()
                for obj in qryResult:
                    key = type(obj).__name__ + '.' + obj.id
                    dictionary[key] = obj

        return dictionary

    def new(self, obj):
        """
            Add a new object to the database
        """
        self.__session.add(obj)

    def save(self):
        """
            Commit changes to the database
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete an object from the database
        """
        if obj:
            self.__session.query(type(obj)).filter_by(id=obj.id).delete()

    def reload(self):
        """
            Recreate all objects from the database
        """
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()
