from flask import render_template, redirect, session, flash
from flask_login import login_user, login_required, logout_user, current_user

from models import Employee, Ride

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


@login_required
def index():
    rides = Ride.query.all()
    return render_template('general/show_rides.html', rides=rides, title='Fahrplan')


@login_required
def plan():
    rides = Employee.query.filter_by(id=current_user.get_id()).first().rides
    return render_template('general/show_rides.html', rides=rides, title='Dienstplan {}'.format(current_user.name))


def login():
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(name=form.username.data).first()
        if employee:
            if employee.password == form.password.data:
                login_user(employee)
                return redirect('/')
        flash('Falsche Login-Daten!')
        return redirect('/login')
    return render_template('general/login.html', form=form)


@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    return redirect('/login')


def get_rides():
    return {'data': [ride.to_dict() for ride in Ride.query]}
