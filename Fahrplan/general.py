from flask import render_template, url_for
from flask_login import login_user
from werkzeug.utils import redirect

from Models import Employee
from login import LoginForm

def index():
    return render_template('index.html')

def login():
    form = LoginForm()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(name=form.username.data).first()
        if employee:
            #if check_password_hash(user.password, form.password.data):
            if (employee.password, form.password.data):
                login_user(employee, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)