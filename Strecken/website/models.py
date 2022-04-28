from sqlalchemy import ForeignKey

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    #stations = db.relationship('Stations')

class Routes(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True) #autoincrement=True ?
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Sections(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    distance = db.Column(db.Integer)
    maxSpeed = db.Column(db.Integer)
    fee = db.Column(db.Float)
    startStation = (db.String(100), ForeignKey('stations.id'))
    endStation = (db.String(100), ForeignKey('stations.id'))

    def __init__(self, name, distance, maxSpeed, fee, startStation, endStation):
        self.name = name
        self.distance = distance
        self.maxSpeed = maxSpeed
        self.fee = fee
        self.startStation = startStation
        self.endStation = endStation

    def __repr__(self):
        return self.name

class Stations(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, address):
        self.name = name
        self.address = address
        #self.user_id = user_id

    def __repr__(self):
        return self.name

class RouteSections(db.Model):
    __tablename__ = 'routeSections'
    route = db.Column(db.String(100), ForeignKey('routes.id'), primary_key=True)
    section = db.Column(db.String(100), ForeignKey('sections.id'), primary_key=True)

    def __init__(self, route, section):
        self.route = route
        self.section = section
