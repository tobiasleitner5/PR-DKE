from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #for relationship one-to-many: get all tickets from a user
    tickets = db.relationship('Ticket', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=mp&s={}'.format(digest, size)

    def bought_tickets(self):
        tickets = Ticket.query.filter_by(user_id=self.id)
        return tickets


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))