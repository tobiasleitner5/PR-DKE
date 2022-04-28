from flask import render_template, redirect, session, flash
from flask_login import login_user, login_required, logout_user

from models import Employee
from login import LoginForm
from flask_login import current_user

@login_required
def index():
    return render_template('index.html', current_user=current_user)

def login():
    form = LoginForm()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(name=form.username.data).first()
        if employee:
            #TODO: Passwörter als HASH speichern. if check_password_hash(user.password, form.password.data):
            if (employee.password, form.password.data):
                login_user(employee)
                return redirect('/')

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect('/login')
