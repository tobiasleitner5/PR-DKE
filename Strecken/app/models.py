from datetime import datetime
from hashlib import md5

from flask import url_for
from flask_login import UserMixin, current_user
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.utils import redirect

from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

# flask db init
# flask db migrate -m "first migrate"
# flask db upgrade
# pbkdf2:sha256:260000$AVcGgBYvr3vX5zUz$38f7b51af557748d3ebe4e947acd1d5967567257199fa390317348019cc63f6b

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Stations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    section1 = relationship("Sections", backref="start_station", foreign_keys='Sections.start_station_id')
    section2 = relationship("Sections", backref="end_station", foreign_keys='Sections.end_station_id')

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }


class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    distance = db.Column(db.Integer)
    maxSpeed = db.Column(db.Integer)
    fee = db.Column(db.Float)
    is_schmalspur = db.Column(db.Boolean)
    warning_id = db.Column(db.Integer, ForeignKey('warnings.id'))
    route_id = db.Column(db.Integer, ForeignKey('routes.id'))
    start_station_id = db.Column(db.Integer, ForeignKey('stations.id'))
    end_station_id = db.Column(db.Integer, ForeignKey('stations.id'))

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
            'route_id': self.route_id,
            'warning_id': self.warning_id
        }

    def __repr__(self):
        return self.name


class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    #warning_id = db.Column(db.Integer, db.ForeignKey('warnings.id'))
    sections = relationship("Sections", backref="routes")
    warnings = relationship("Warnings", backref="routes")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return self.name


class Warnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    sections = relationship("Sections", backref="warnings")
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))

#**********************************************************

class MyModelView(ModelView):
    def is_accessible(self):
        #return current_user.is_admin
        return True

class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return redirect("/admin/routes")

admin = Admin(app,
    index_view=MyAdminIndexView(),
              name="Entitiy Management"
)

admin.add_view(MyModelView(Routes, db.session))
admin.add_view(MyModelView(Sections, db.session))
admin.add_view(MyModelView(Stations, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Warnings, db.session))
# admin.add_view(MyModelView(RouteSections, db.session))
