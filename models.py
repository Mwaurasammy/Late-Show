from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class SerializerMixin:
    def to_dict(self, include_details=False):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Episode(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime)
    number = db.Column(db.Integer)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete')

    def to_dict(self, include_appearances=False):
        episode_dict = super().to_dict()
        if include_appearances:
            episode_dict["appearances"] = [appearance.to_dict(include_details=True) for appearance in self.appearances]
        return episode_dict

class Guest(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete')

    def to_dict(self):
        return super().to_dict()

class Appearance(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    def to_dict(self, include_details=False):
        appearance_dict = super().to_dict()
        if include_details:
            appearance_dict["guest"] = self.guest.to_dict()
            appearance_dict["episode"] = self.episode.to_dict()
        return appearance_dict
