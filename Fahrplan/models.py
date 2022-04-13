from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Rides(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    interval = db.Column(db.Boolean)
    interval_number = db.Column(db.Integer)
    sections = db.Column(db.PickleType, nullable=False) #mutable

    def __init__(self, id, route_id, time, price, interval, interval_nr, sections):
        self.time = time
        self.price = price
        self.interval = interval
        self.interval_number = interval_nr
        self.sections = sections
        self.id = id
        self.route_id = route_id

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    mail = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, mail, password):
        self.name = name
        self.mail = mail
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail,
            'password': self.password
        }

class Crew(db.Model): #table for relationship employee and ride
    __tablename__ = 'crew'
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), primary_key=True)
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)

class Ride_section(db.Model): #table for relationship between ride and section
    __tablename__ = 'ride_sections'
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)
    section_id = db.Column(db.Integer, primary_key=True)