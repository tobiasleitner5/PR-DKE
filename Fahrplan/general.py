from flask import render_template, redirect, session, flash
from flask_login import login_user, login_required, logout_user, current_user

import ReadInput
from models import Employee, Ride, Crew, Ride_section
from login import LoginForm

@login_required
def index():
    # show diensplan
    selected_ride_ids = []
    # get crews
    for c in Crew.query:
        if c.employee_id == int(current_user.get_id()):
            selected_ride_ids.append(c.ride_id)

    selected_rides = []
    # get rides
    for r in Ride.query:
        if r.id in selected_ride_ids:
            selected_rides.append(r)

    selected_ride_sections = []
    for rs in Ride_section.query:
        if rs.ride_id in selected_ride_ids:
            selected_ride_sections.append(rs)

    routes = dict(ReadInput.get_routes_mock())['routes']
    sections = dict(ReadInput.get_sections_mock())['sections']

    entry = []

    for sr in selected_rides:
        route_name = None
        time = sr.time
        sections = None
        for route in routes:
            if int(route['id']) == int(sr.route_id):
                route_name = route['name']

        entry.append(Plan_entry(route_name, time, sections))

    return render_template('index.html', current_user=current_user, rides=entry)

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

class Plan_entry:
   def __init__(self, route_name, time, sections):
       self.route_name = route_name
       self.time = time
       self.sections = sections
