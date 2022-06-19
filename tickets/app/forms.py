from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, TimeField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from datetime import datetime
import api

# sets the fields of the Login Form used for User Log-in
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# sets the fields of the Registration Form used for User Registration
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

# sets the fields of the Edit Profile Form that allows the User to edit his personal data (username, password etc.)
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

# sets the fields of the Ticket Form that allows to search for specific rides
class TicketForm(FlaskForm):
    departure = SelectField('Von', choices=api.getStations(), validators=[DataRequired()])
    destination = SelectField('Nach', choices=api.getStations(), validators=[DataRequired()])
    date = DateField('Wann', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired('please select startdate')])
    time = TimeField('Wann', format='%H:%M', default=datetime.today, validators=[DataRequired()])
    submit = SubmitField('Suchen')

# sets the fields of the Login Form used for User Log-in
class PromotionForm(FlaskForm):
    start_date = DateField('Von', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired('please select startdate')])
    end_date = DateField('Bis', format='%Y-%m-%d', default=datetime.today, validators=[DataRequired('please select enddate')])
    sale = IntegerField('Promotion [%]', validators=[DataRequired('Prozentsatz zwischen 1 und 100'), NumberRange(min=1, max=100)])
    route = SelectField('Choose section if applicable:', choices=api.get_route_name(), validators=[DataRequired()])
    validity = RadioField('Label', choices=['Preisnachlass für alle Fahrtstrecken', 'Preisnachlass für ausgewählte Fahrtstrecke'], default = 'Preisnachlass für alle Fahrtstrecken', validators=[DataRequired()])
    submit = SubmitField('Aktion festlegen')

    def validate_start_date(self, start_date):
        today = datetime.now()
        if start_date.data < today.date():
            raise ValidationError('Der gewählte Tag liegt in der Vergangenheit.')

    def validate_end_date(self, end_date):
        today = datetime.now()
        if end_date.data < today.date():
            raise ValidationError('Der gewählte Tag liegt in der Vergangenheit.')
        elif self.start_date.data > end_date.data:
            raise ValidationError('Das Enddatum ist vor dem Startdatum.')

# sets the fields of the Empty Form used for different contexts
class EmptyForm(FlaskForm):
    cancel = SubmitField('Abbrechen')
    submit = SubmitField('Submit')
