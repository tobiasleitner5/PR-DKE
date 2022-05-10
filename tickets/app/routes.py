from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, TicketForm, EditProfileForm, EmptyForm, TicketOverviewForm
from flask_login import current_user, login_user
from app.models import User, Ticket
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from flask import request
from werkzeug.urls import url_parse
import api

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TicketForm()
    if form.validate_on_submit():
        start = form.departure.data
        end = form.destination.data
        succ = False
        res = []
        for r in api.get_rides()["data"]:
            l = api.get_sections_by_route_id(r["route_id"])
            lStations = []
            for s in l:
                lStations.append(s["name"])
            if lStations.__contains__(start) and lStations.__contains__(end) and lStations.index(
                    start) < lStations.index(end) and start != end:
                succ = True
                res.append(r)
        if not succ:
            flash("Keine Fahrtdurchführung gefunden!")
        return render_template("index.html", title='Home Page', result=True, form=form, results=res)
    return render_template("index.html", title='Home Page', results=False, form=form)

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
    return render_template('login.html', title='Sign In', form=form)

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

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form = EditProfileForm(current_user.username, current_user.email)
    user = User.query.filter_by(id=int(current_user.id)).first_or_404()
    if form.delete.data:
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted your profile!')
        return redirect(url_for('logout'))
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your username and email have been saved.')
        if form.oldPassword.data and not user.check_password(form.oldPassword.data):
            flash('Your old password does not match.')
            return redirect(url_for('user', username=current_user.username))
        if form.newPassword.data and user.check_password(form.oldPassword.data):
            current_user.set_password(form.newPassword.data)
            db.session.commit()
            flash('Your password has been changed.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('user.html', user=user, title='Profile', form=form)

@app.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketOverviewForm()
    tickets=current_user.bought_tickets()
    return render_template('tickets.html', title='My Tickets', form=form, tickets=tickets)

@app.route('/cancelticket/<ticketid>', methods=['GET', 'POST'])
@login_required
def cancelticket(ticketid):
    form = EmptyForm()
    ticket = Ticket.query.filter_by(id=ticketid).first()
    if form.cancel.data:
        return redirect(url_for('index'))
    if form.submit.data:
        if ticket.status == 'active':
            ticket.set_status('cancelled')
            db.session.commit()
            flash("Das Ticket wurde erfolgreich storniert.")
        else:
            flash("Das Ticket ist bereits storniert oder wurde bereits verbraucht.")
        return redirect(url_for('tickets'))
    return render_template('cancelticket.html', title='My Tickets', form=form)

@app.route('/buyticket/<rideid>', methods=['GET', 'POST'])
@login_required
def buyticket(rideid):
    form = EmptyForm()
    if form.cancel.data:
        return redirect(url_for('index'))
    if form.submit.data:
        ticket = Ticket(user_id=current_user.id, ride_id=rideid)
        db.session.add(ticket)
        db.session.commit()
        flash('Das Ticket wurde erfolgreich erworben!')
        return redirect(url_for('tickets'))
    return render_template('buyticket.html', title='Buy Ticket', form=form)
