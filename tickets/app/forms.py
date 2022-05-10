from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from datetime import datetime
import api

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    oldPassword = PasswordField('Old Password')
    newPassword = PasswordField('New Password')
    newPassword2 = PasswordField('Repeat new Password', validators=[EqualTo('newPassword')])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')

class TicketForm(FlaskForm):
    departure = SelectField('Von', choices=api.getStartStations(), validators=[DataRequired()])
    destination = SelectField('Nach', choices=api.getEndStations(), validators=[DataRequired()])
    date = DateField('Wann', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired('please select startdate')])
    time = TimeField('Wann', format='%H:%M', default=datetime.today, validators=[DataRequired()])
    submit = SubmitField('Suchen')

class BuyTicketForm(FlaskForm):
    cancel = SubmitField('Abbrechen')
    buy = SubmitField('Kaufen')

class TicketOverviewForm(FlaskForm):
    book_seat = SubmitField('Sitzplatz buchen')
    cancel_ticket = SubmitField('Stornieren')


