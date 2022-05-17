from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import api
from flask import flash
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #access as either user or admin
    access = db.Column(db.Enum('user', 'admin'), nullable=False, server_default='user')
    #for relationship one-to-many: get all tickets from a user
    tickets = db.relationship('Ticket', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_access(self, access):
        self.access = access

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.access == 'admin'

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)

    def bought_tickets(self):
        tickets = Ticket.query.filter_by(user_id=self.id)
        return tickets
    
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'access': self.access
        }


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ride_id = db.Column(db.Integer)
    status = db.Column(db.Enum('active','cancelled','used'), nullable=False, server_default="active")
    seat = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Ticket {}>'.format(self.id)

    def set_status(self, status):
        self.status = status

    def set_seat(self, seat):
        self.seat = seat

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    sale = db.Column(db.Integer)
    all_routes = db.Column(db.Boolean, default=False)
    route_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Promotion {} {} {} {} {} {}>'.format(self.id,self.sale,self.start_date,self.end_date,self.route_id,self.all_routes)

    def set_all_routes(self, all_routes):
        self.all_routes = all_routes
        
    def set_route_id(self, route_id):
        self.route_id = route_id

    def get_route_name(self):
        return api.get_route_name_by_id(self.route_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))