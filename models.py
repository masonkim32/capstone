import json
import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine

database_name = 'castingagency'
database_path = 'postgres://{}:{}@{}/{}'.format(
    'castingagency',
    'castingagency',
    '127.17.0.2:5432',
    database_name
)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """setup_db(app)

    binds a flask application and a SQLAlchemy service

    Arguments:
        app (obj): flask app object
        database_path (str): database path
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(db.DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.answer,
            'release_date': self.release_date,
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
