import json

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user

from app.models import User, Sections, Routes, Warnings
from app import app
from app.forms import LoginForm, AddSection, AddWarning
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.models import Stations


@app.route('/index')
@login_required
def index():
    routes = db.session.query(Routes)
    route_sec = db.session.query(Routes.sections)
    return render_template('routes.html', title='Routes', user=current_user, routes=routes, route_sec=route_sec)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, user=current_user)


# Documentation: This method is used to add sections to a route. First of all the end station of the last section of the
# route is retrieved. Then all sections are retrieved from the database. If the last station is not null, sections with
# the same start station as the last end station are put into a list. The select box is then filled with
# the list of these sections. This makes sure that all sections are connected. If the user clicks submit,
# the new section is added to the route.
@app.route('/add_section/<name>', methods=['GET', 'POST'])
def addSection(name):
    route = Routes.query.filter_by(name=name).first_or_404()
    lastStation = 0
    for s in route.sections:
        lastStation = s.end_station_id
    all_sections = db.session.query(Sections)
    sections_list = [(i.id, i.name) for i in all_sections]
    if (not not lastStation):
        sections = db.session.query(Sections).filter(Sections.start_station_id == lastStation).all()
        sections_list = [(i.id, i.name) for i in sections]
    form = AddSection()
    form.section.choices = sections_list
    if form.validate_on_submit():
        for s1 in all_sections:
            if (s1.id == form.section.data): new_section = s1
        route.sections.append(new_section)
        db.session.commit()
        return redirect(url_for('routes'))
    return render_template('add_sections.html', title='Add Sections', user=current_user, form=form, route=route)


# Documentation: This method is used to add warnings to a route. First of all a list with all warnings is created,
# then all warnings of the route are retrieved. These two lists are compared by turning the lists into sets and
# using the .difference method of sets, this way only warnings who have not been added to a route yet can be selected.
# The selection box is then filled with these warnings. If the user clicks on submit the warning is added to the route.
@app.route('/add_warning_route/<name>', methods=['GET', 'POST'])
def addWarningRoute(name):
    route = Routes.query.filter_by(name=name).first_or_404()
    all_warnings = db.session.query(Warnings)
    warnings_list = [(i.id, i.name) for i in all_warnings]
    warnings_list_route = [(i.id, i.name) for i in route.warnings_link]
    setAllW = set(warnings_list)
    setRW = set(warnings_list_route)
    newList = list(setAllW.difference(setRW))
    form = AddWarning()
    form.warning.choices = newList
    if form.validate_on_submit():
        for s1 in all_warnings:
            if s1.id == form.warning.data: new_warning = s1
        route.warnings_link.append(new_warning)
        db.session.commit()
        return redirect(url_for('routes'))
    return render_template('add_warning_route.html', title='Add Warnings', user=current_user, form=form, route=route)


# Documentation: This method is used to add warnings to a section, the same logic as in addWarningsRoute is used.
@app.route('/add_warning_section/<name>', methods=['GET', 'POST'])
def addWarningSection(name):
    section = Sections.query.filter_by(name=name).first_or_404()
    all_warnings = db.session.query(Warnings)
    warnings_list = [(i.id, i.name) for i in all_warnings]
    warnings_list_route = [(i.id, i.name) for i in section.warnings_link]
    setAllW = set(warnings_list)
    setRW = set(warnings_list_route)
    newList = list(setAllW.difference(setRW))
    form = AddWarning()
    form.warning.choices = newList
    if form.validate_on_submit():
        for s1 in all_warnings:
            if s1.id == form.warning.data: new_warning = s1
        section.warnings_link.append(new_warning)
        db.session.commit()
        return redirect(url_for('routes'))
    return render_template('add_warning_section.html', title='Add Warnings', user=current_user, form=form,
                           section=section)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/stations')
@login_required
def stations():
    stations = db.session.query(Stations)
    return render_template('stations.html', title='Stations', user=current_user, stations=stations)


@app.route('/sections')
@login_required
def sections():
    sections = db.session.query(Sections)
    stations = db.session.query(Stations)
    return render_template('sections.html', title='Sections', user=current_user, sections=sections, stations=stations)


@app.route('/')
@app.route('/routes')
@login_required
def routes():
    routes = db.session.query(Routes)
    route_sec = db.session.query(Routes.sections)
    return render_template('routes.html', title='Routes', user=current_user, routes=routes, route_sec=route_sec)


@app.route('/stations/get')
def get_stations():
    return {'stations': [station.to_dict() for station in Stations.query]}


@app.route('/sections/get')
def get_sections():
    return {'sections': [section.to_dict() for section in Sections.query]}


@app.route('/routes/get')
def get_rotues():
    return {'routes': [route.to_dict() for route in Routes.query]}


@app.route('/warnings/get')
def get_warnings_sections():
    return {'warnings': [warning.to_dict() for warning in Warnings.query]}


@app.route('/trains', methods=['GET'])
def getTrains():
    json_file = open('./trains.json')
    data = json.load(json_file)
    return data
