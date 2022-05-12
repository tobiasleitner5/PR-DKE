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
# flask db migrate -m "users table"
# flask db upgrade

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Stations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))

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
    startStation = (db.String(100), ForeignKey('stations.id'))
    endStation = (db.String(100), ForeignKey('stations.id'))
    is_schmalspur = db.Column(db.Boolean)
    warning_id = db.Column(db.Integer, db.ForeignKey('warnings.id'))

    def to_dict(self):
        return {
            'name': self.name,
            'distance': self.distance,
            'maxSpeed': self.maxSpeed,
            'fee': self.fee,
            'startStation': self.startStation,
            'endStation': self.endStation
        }

    def __repr__(self):
        return self.name


class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    warning_id = db.Column(db.Integer, db.ForeignKey('warnings.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return self.name


class RouteSections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

    route = relationship(Routes, backref=backref("sections", cascade="all, delete-orphan"))
    section = relationship(Sections, backref=backref("route", cascade="all, delete-orphan"))

    def __init__(self, route, section):
        self.route = route
        self.section = section


class Warnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))

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
admin.add_view(MyModelView(RouteSections, db.session))
