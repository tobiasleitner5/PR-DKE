import json

from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user

from app.models import User, Sections, Routes, Warnings, routes_sections
from app import app
from app.forms import LoginForm, EmptyForm, EditStationForm, NewStationForm, AddSection
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
from app.models import Stations


@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user)


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
    return redirect(url_for('index'))


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
    return render_template('register.html', title='Register', form=form)


@app.route('/add_section/<name>', methods=['GET', 'POST'])
def addSection(name):
    route = Routes.query.filter_by(name=name).first_or_404()
    lastStation = 0
    for s in route.sections:
        lastStation=s.end_station_id
    sections = db.session.query(Sections).filter(Sections.start_station_id == lastStation).all()
    all_sections = db.session.query(Sections)
    sections_list = [(i.id, i.name) for i in sections]
    form = AddSection()
    form.section.choices = sections_list
    if form.validate_on_submit():
        new_section = route.sections[0]
        for s1 in all_sections:
            if(s1.id == form.section.data): new_section = s1
        route.sections.append(new_section)
        db.session.commit()
        return redirect(url_for('routes'))
    return render_template('add_sections.html', title='Add Sections', user=current_user, form=form, route=route)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


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


@app.route('/warnings/get/sections')
def get_warnings_sections():
    warnings = db.session.query(Warnings)
    return render_template('sections_warnings.html', title='Warnings', user=current_user, warnings=warnings)


@app.route('/warnings/get/routes')
def get_warnings_routes():
    warnings = db.session.query(Warnings)
    return render_template('routes_warnings.html', title='Warnings', user=current_user, warnings=warnings)


@app.route('/trains', methods=['GET'])
def getTrains():
    json_file = open('./trains.json')
    data = json.load(json_file)
    return data

