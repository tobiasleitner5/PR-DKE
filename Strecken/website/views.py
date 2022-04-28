from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from .models import Note, Stations
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/routes', methods=['GET', 'POST'])
def routes():
    return render_template("routes.html", user=current_user)


@views.route('/sections', methods=['GET', 'POST'])
def sections():
    return render_template("sections.html", user=current_user)


@views.route('/stations', methods=['GET', 'POST'])
def stations():
    return render_template("stations.html", user=current_user)


@views.route('/users', methods=['GET', 'POST'])
def users():
    return render_template("users.html", user=current_user)

@views.route('/new_station', methods=['GET', 'POST'])
def new_station():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')

        # todo: check name and address - length etc.
        #user = User.query.filter_by(email=email).first()
        # if user:
        #    flash('Email already exists.', category='error')
        # elif len(email) < 4:
        #    flash('Email must be longer than 3 characters!', category='error')
        new_stations = Stations(name=name, address=address)
        db.session.add(new_stations)
        db.session.commit()
        flash('Station created!', category='success')
        return redirect(url_for('views.home'))

    return render_template("new_station.html", user=current_user)


@views.route('/edit_station', methods=['GET', 'POST'])
def edit_station():
    return render_template("edit_station.html", user=current_user)