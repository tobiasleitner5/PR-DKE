from app import app, db
from flask import render_template, flash, redirect, url_for, session
from app.forms import LoginForm, TicketForm, EditProfileForm, PromotionForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ticket, Promotion
from app.admin_decorator import requires_access
from app.forms import RegistrationForm
from flask import request
from werkzeug.urls import url_parse
import api
from datetime import datetime, date

# main index view to search for tickets/ show results
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('promotion'))
    form = TicketForm()
    if form.validate_on_submit():
        # if the Search for Ticket Form is submitted, the system searches for possible trips
        start = int(api.getStationsByName(form.departure.data)["id"])
        end = int(api.getStationsByName(form.destination.data)["id"])
        date = form.date.data
        time = form.time.data
        succ = False
        res = []
        promotions = Promotion.query.all()
        warnings_dict = {}
        # get all rides and search for suitable ones based on the criteria of the submitted form
        for r in api.get_rides()["data"]:
            planned_route = api.get_planned_route_by_id(r["plannedroute_id"])
            ride_time = datetime.strptime(r["time"], "%a, %d %b %Y %H:%M:%S GMT")
            full_ride = False
            append = False
            lSections = []
            route = api.get_routeid_by_sections(planned_route["sections"])
            # the following code orders sections from a ride so that it is possible to search for stations included in a route
            ordered_sections = [item for item in route["sections"] if item in planned_route["sections"]]
            for s in ordered_sections:
                section = api.get_section_by_id(s)
                if section["startStation"] == start or append:
                    full_ride = True
                    append = True
                    lSections.append(s)
                if section["endStation"] == end:
                    append = False
                    lSections.append(s)
            # checks for time compatibility
            if full_ride and not append and ride_time.date() == date and ride_time.time() >= time:
                lSections = list(set(lSections))
                r["price"] = r["price"] * (len(lSections)/len(ordered_sections))
                res.append(r)
                succ = True
                # gets a dict with all warnings associated with a ride
                warnings_dict[r["id"]] = get_warnings_section(lSections, route)
        if not succ:
            flash("Keine Fahrtdurchführung gefunden!")
        return render_template("index.html", title='Home Page', result=True, form=form, results=res, promotions=promotions, pricedict=get_best_promo(), warnings=warnings_dict)
    return render_template("index.html", title='Home Page', results=False, form=form)

# get list of all possible warnings for a ride (included warnings of sections and route)
def get_warnings_section(list_sections, route):
    list = []
    warnings = api.get_warnings()
    for w in warnings["warnings"]:
        if any(item in w["sections"] for item in list_sections) or (route["id"] in w["routes"]):
            list.append(w["name"])
    return list

# get a dictionary with the best promotion matched to the ride id
def get_best_promo():
    best_promo_dict = {}
    for r in api.get_rides()["data"]:
        list_routes = api.get_route_of_ride(r["plannedroute_id"])
        best_promo = get_best_promo_by_route(list_routes, r["time"])
        best_promo_dict[r["id"]] = best_promo
    return best_promo_dict

# sub function of get_best_promo() -> checks if time slot is suitable
def get_best_promo_by_route(list_routes, ride_time_str):
    promotions = Promotion.query.all()
    best_promo = 0
    for p in promotions:
        ride_time = datetime.strptime(ride_time_str, "%a, %d %b %Y %H:%M:%S GMT").date()
        if p.start_date <= ride_time <= p.end_date:
            if p.all_routes and p.sale > best_promo:
                best_promo = p.sale
            elif list_routes.__contains__(p.route_id) and p.sale > best_promo:
                best_promo = p.sale
    return best_promo

# setting the login page including checking if the entered data is valid
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

# logs the User out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# setting the registration page including adding a new user to the database
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

# loads the profile form of a specific user and allows editing personal data
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

# loads the ticket page where an overview of all bought tickets is given
@app.route('/tickets', methods=['GET', 'POST'])
@requires_access('user')
@login_required
def tickets():
    tickets=current_user.bought_tickets()
    today = datetime.now()
    for t in tickets:
        rideid = t.ride_id
        ride_time = datetime.strptime(api.get_ride_by_id(rideid)["time"],"%a, %d %b %Y %H:%M:%S GMT")
        if t.status == 'active' and t.status != 'used' and ride_time < today:
            t.set_status('used')
            db.session.commit()
    ticketid = request.args.get('ticketid')
    book_seat(ticketid)
    return render_template('tickets.html', title='My Tickets', tickets=tickets)

# function for booking a seat by given ticket id
def book_seat(ticketid):
    ticket = Ticket.query.filter_by(id=ticketid).first()
    if ticket is not None and ticket.status == 'active':
        rideid = ticket.ride_id
        booked_seats = len(Ticket.query.filter_by(ride_id=rideid, seat=True).all())
        trainid = api.get_ride_by_id(rideid)["train_id"]
        available_seats = api.get_train_by_id(trainid)["seats"]
        if ticket.seat:
            flash("Sitzplatz bereits gebucht!")
        elif available_seats <= booked_seats:
            flash("Alle Sitzplätze sind bereits vergeben!")
        elif not ticket.seat:
            ticket.set_seat(True)
            db.session.commit()
            flash("Sitzplatz erfolgreich reserviert!")
    elif ticket is not None:
        flash("Das Ticket ist nicht mehr verfügbar, da storniert oder verbraucht!")

# function for cancelling a ticket by given ticket id
@app.route('/cancelticket/<ticketid>', methods=['GET', 'POST'])
@requires_access('user')
@login_required
def cancelticket(ticketid):
    form = EmptyForm()
    ticket = Ticket.query.filter_by(id=ticketid).first()
    if form.cancel.data:
        return redirect(url_for('tickets'))
    if form.submit.data:
        if ticket.status == 'active':
            ticket.set_seat(False)
            ticket.set_status('cancelled')
            db.session.commit()
            flash("Das Ticket wurde erfolgreich storniert.")
        else:
            flash("Das Ticket ist bereits storniert oder wurde bereits verbraucht.")
        return redirect(url_for('tickets'))
    return render_template('cancelview.html', title='My Tickets', form=form, question="Möchten Sie das Ticket stornieren?")

# function for canceling a promotion by given promotion id (access level admin)
@app.route('/cancelpromo/<promotionid>', methods=['GET', 'POST'])
@requires_access('admin')
@login_required
def cancelpromo(promotionid):
    form = EmptyForm()
    promotion = Promotion.query.filter_by(id=promotionid).first()
    if form.cancel.data:
        return redirect(url_for('overview'))
    if form.submit.data:
        db.session.delete(promotion)
        db.session.commit()
        flash('Die Aktion wurde erfolgreich gelöscht!')
        return redirect(url_for('overview'))
    return render_template('cancelview.html', title='My Promotion', form=form, question="Möchten Sie die Aktion löschen?")

# function for buying a ticket by given ride id, departure and destination
@app.route('/buyticket/<rideid>/<departure>/<destination>', methods=['GET', 'POST'])
@requires_access('user')
@login_required
def buyticket(rideid,departure,destination):
    form = EmptyForm()
    today = datetime.now()
    ride_time = datetime.strptime(api.get_ride_by_id(int(rideid))["time"], "%a, %d %b %Y %H:%M:%S GMT")
    if ride_time < today:
        flash("Ticketkauf fehlgeschlagen! Die Reise liegt in der Vergangenheit.")
        return redirect(url_for('index'))
    elif form.cancel.data:
        return redirect(url_for('index'))
    elif form.submit.data:
        ticket = Ticket(user_id=current_user.id, ride_id=rideid, departure=departure, destination=destination)
        db.session.add(ticket)
        db.session.commit()
        flash('Das Ticket wurde erfolgreich erworben!')
        return redirect(url_for('tickets'))
    return render_template('buyticket.html', title='Buy Ticket', form=form)

# loads the promotion page for setting promotions (access level admin)
@app.route('/promotion', methods=['GET', 'POST'])
@requires_access('admin')
@login_required
def promotion():
    form = PromotionForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        sale = form.sale.data
        promotion = Promotion(start_date=start_date, end_date=end_date, sale=sale)
        if form.validity.data == 'Preisnachlass für alle Fahrtstrecken':
            promotion.set_all_routes(True)
        else:
            route_id = api.get_route_id_by_name(form.route.data)
            promotion.set_route_id(route_id)
        db.session.add(promotion)
        db.session.commit()
        return redirect(url_for('overview'))
    return render_template('promotion.html', title='Set Promotion', form=form)

# loads the overview form to see all promotions (access level admin)
@app.route('/overview', methods=['GET', 'POST'])
@requires_access('admin')
@login_required
def overview():
    promotions = Promotion.query.all()
    return render_template('overview.html', title='Overview Promotion', promotions=promotions)


# used for testing purpose to get all users
#@app.route('/get/users')
#def users():
#    return {'data': [user.to_json() for user in User.query]}