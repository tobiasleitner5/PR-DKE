from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Routes(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True) #autoincrement=True ?
    name = db.Column(db.String(100))

class Sections(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    distance = db.Column(db.Integer)
    maxSpeed = db.Column(db.Integer)
    fee = db.Column(db.Float)
    startStation = (db.String(100), ForeignKey('stations.id'))
    endStation = (db.String(100), ForeignKey('stations.id'))


class Stations(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))

class RouteSections(db.Model):
    __tablename__ = 'routeSections'
    route = db.Column(db.String(100), ForeignKey('routes.id'), primary_key=True)
    section = db.Column(db.String(100), ForeignKey('sections.id'), primary_key=True)
