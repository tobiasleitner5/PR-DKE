from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    interval = db.Column(db.Boolean)
    interval_number = db.Column(db.Integer)

    def __init__(self, route_id, time, price, interval, interval_nr):
        self.time = time
        self.price = price
        self.interval = interval
        self.interval_number = interval_nr
        self.route_id = route_id

    def to_dict(self):
        return {
            'id': self.id,
            'route_id': self.route_id,
            'time': self.time,
            'price': self.price,
            'interval': self.interval,
            'interval_number': self.interval_number
        }

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    mail = db.Column(db.String)
    password = db.Column(db.String)
    is_admin = db.Column(db.Boolean)

    def __init__(self, name, mail, password, is_admin):
        self.name = name
        self.mail = mail
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return self.name + ', ' + str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail,
            'password': self.password,
            'is_admin': self.is_admin
        }

    @property
    def is_admin_check(self):
        return self.is_admin

class Crew(db.Model): #table for relationship employee and ride
    __tablename__ = 'crew'
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), primary_key=True)
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)

    def __init__(self, ride_id, employee_id):
        self.ride_id = ride_id
        self.employee_id = employee_id

class Ride_section(db.Model): #table for relationship between ride and section
    __tablename__ = 'ride_sections'
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)
    section_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, ride_id, section_id):
        self.ride_id = ride_id
        self.section_id = section_id
