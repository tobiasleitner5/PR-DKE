from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

crew = db.Table('crew',
                db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
                db.Column('ride_id', db.Integer, db.ForeignKey('rides.id'))
                )

plannedroutes_sections = db.Table('plannedroutes_sections',
                                  db.Column('planned_route_id', db.Integer, db.ForeignKey('plannedroutes.id')),
                                  db.Column('sections_id', db.Integer, db.ForeignKey('sections.id'))
                                  )


class Train(db.Model):
    __tablename__ = 'trains'
    id = db.Column(db.Integer, primary_key=True)
    is_normalspur = db.Column(db.Boolean)
    maxWidth = db.Column(db.Float)
    name = db.Column(db.String(100))
    seats = db.Column(db.Integer)
    ride = relationship("Ride", backref="trains")

    def __init__(self, id, name, maxWidth, is_normalspur, seats):
        self.id = id
        self.name = name
        self.maxWidth = maxWidth
        self.is_normalspur = is_normalspur
        self.seats = seats

    @staticmethod
    def from_json(json_dct):
        trains = []
        for t in json_dct:
            trains.append(Train(t['id'], t['name'], t['maxWidth'], t['isNormalspur'], t['seats']))
        return trains

    def __repr__(self):
        return self.name + ', ' + str(self.id)


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


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sections = relationship("Section", backref="routes")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return self.name

    @staticmethod
    def from_json(json_dct):
        routes = []
        for r in json_dct:
            routes.append(Route(r['id'], r['name']))
        return routes


class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plannedroute_id = db.Column(db.Integer, ForeignKey('plannedroutes.id'))
    plannedroute = db.relationship("PlannedRoute")
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    interval = db.Column(db.Boolean)
    train_id = db.Column(db.Integer, ForeignKey('trains.id'))
    executed_by = db.relationship('Employee', secondary=crew, backref='rides')

    def __init__(self, plannedroute_id, time, price, interval, train_id):
        self.time = time
        self.price = price
        self.interval = interval
        self.plannedroute_id = plannedroute_id
        self.train_id = train_id

    def to_dict(self):
        #list = PlannedRoute.query.filter_by(id=self.plannedroute_id).first().abschnitte
        #for l in list:
            #print(l.id)
        return {
            'id': self.id,
            'start': 1,
            'end': 2,
            'time': self.time,
            'price': self.price,
            'train_id': self.train_id,
            'interval': self.interval
        }

    def __repr__(self):
        return 'Ride ' + str(self.id)


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    section1 = relationship("Section", backref="start_station", foreign_keys='Section.start_station_id')
    section2 = relationship("Section", backref="end_station", foreign_keys='Section.end_station_id')

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }

    @staticmethod
    def from_json(json_dct):
        stations = []
        for s in json_dct:
            stations.append(Station(s['id'], s['name'], s['address']))
        return stations


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    distance = db.Column(db.Integer)
    maxSpeed = db.Column(db.Integer)
    fee = db.Column(db.Float)
    is_schmalspur = db.Column(db.Boolean)
    route_id = db.Column(db.Integer, ForeignKey('routes.id'))
    start_station_id = db.Column(db.Integer, ForeignKey('stations.id'))
    end_station_id = db.Column(db.Integer, ForeignKey('stations.id'))

    def __init__(self, id, name, distance, maxSpeed, fee, is_schmalspur, route_id, start_station_id, end_station_id):
        self.id = id
        self.name = name
        self.distance = distance
        self.maxSpeed = maxSpeed
        self.fee = fee
        self.is_schmalspur = is_schmalspur
        self.route_id = route_id
        self.start_station_id = start_station_id
        self.end_station_id = end_station_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance': self.distance,
            'maxSpeed': self.maxSpeed,
            'fee': self.fee,
            'startStation': self.start_station_id,
            'endStation': self.end_station_id,
            'is_schmalspur': self.is_schmalspur,
            'route_id': self.route_id
        }

    def __repr__(self):
        return self.name

    @staticmethod
    def from_json(json_dct):
        sections = []
        for s in json_dct:
            sections.append(
                Section(s['id'], s['name'], s['distance'], s['maxSpeed'], s['fee'], s['is_schmalspur'], s['route_id'],
                        s['startStation'], s['endStation']))
        return sections


class PlannedRoute(db.Model):
    __tablename__ = 'plannedroutes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    abschnitte = db.relationship('Section', secondary=plannedroutes_sections, backref='planned_routes')

    def __init__(self, name, sections):
        self.name = name
        self.abschnitte.extend(sections)

    def get_sections_info(self):
        isNormalspur = True
        time = 0.0
        fee = 0
        for s in self.abschnitte:
            time = time + float(s.distance) / float(s.maxSpeed)
            fee = fee + s.fee
            if str(s.is_schmalspur) == 'True':
                isNormalspur = False

        data = {
            'isNormalspur': isNormalspur,
            'time': time,
            'fee': fee
        }
        return data

    def __repr__(self):
        return self.name
