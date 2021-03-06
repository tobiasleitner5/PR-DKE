from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from collections import namedtuple

from models import Route, PlannedRoute, Train, Ride, Employee, Section, db, Station


###### VIEWS ######

class AllAdminBaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False


class AllAdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False


class PlanRideView(AllAdminBaseView):
    @expose('/')
    def index(self):
        column_names = ['ID', 'Name', 'Abschnitte', 'Einzel-Fahrtdurchführung planen',
                        'Intervall-Fahrtdurchführung planen']
        plan_routes = PlannedRoute.query.all()
        return self.render('admin/admin_plannedroutes_overview.html', records=plan_routes, colnames=column_names)


class PlanRouteView(AllAdminBaseView):
    @expose('/')
    def index(self):
        column_names = ['ID', 'Name', 'Planen']
        routes = Route.query.all()
        return self.render('admin/admin_routes_overview.html', records=routes, colnames=column_names)


class RideView(AllAdminModelView):
    can_create = False
    column_labels = dict(plannedroute='Fahrtstrecke', time='Datum und Uhrzeit', price='Preis', interval='Intervall',
                         trains='Zug', executed_by='Mitarbeiter')

    def get_edit_form(self):
        form_class = super(RideView, self).get_edit_form()
        del form_class.interval
        del form_class.plannedroute
        return form_class


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin_check
        else:
            return False


class EmployeeView(AllAdminModelView):
    column_labels = dict(name='Name', mail='Mail', password='Passwort', is_admin='Admin')

    def get_edit_form(self):
        form_class = super(EmployeeView, self).get_edit_form()
        del form_class.rides
        return form_class

    def get_create_form(self):
        form_class = super(EmployeeView, self).get_create_form()
        del form_class.rides
        return form_class


###### ADMIN FUNCITONALITIES ######

def plan_single_ride(plannedroute_id):
    if request.method == 'GET':
        return render_template('admin/plan_single_ride_step1.html', plannedroute_id=plannedroute_id)  # first step
    else:
        time = request.form['time']
        return redirect(
            url_for('store_ride_blueprint.store_ride', time=time, interval='False',
                    plannedroute_id=plannedroute_id))  # get request to store ride mapping


def plan_interval_ride(plannedroute_id):
    if request.method == 'GET':
        return render_template('admin/plan_interval_ride_step1.html', plannedroute_id=plannedroute_id)  # first step
    else:
        start = request.form['start']
        end = request.form['end']
        rep_type = request.form['rep_type']
        return redirect(
            url_for('store_ride_blueprint.store_ride', start=start, end=end, rep_type=rep_type, interval='True',
                    plannedroute_id=plannedroute_id))  # get request to store_ride mapping


# returns a form to create Fahrtstrecken
def plan_route(route_id):
    if request.method == 'GET':
        route = Route.query.filter_by(id=route_id).first()
        sections = route.sections
        stations = []
        end_stations = []
        for section in sections:
            stations.append(section.start_station)
            end_stations.append(section.end_station)

        for e in end_stations:  # insert all stations to stations list. But no duplicates
            if e not in stations:
                stations.append(e)

        return render_template('admin/plan_route.html', title='Plane Fahrtstrecke für Route {}'.format(route.name),
                               sections=sections, routes_id=route_id, stations=stations)


# this method returns all the rides that should be created when defining interval based rides.
def create_interval_rides(plannedroute_id, start, end, rep_type, price, train, fee):
    seats = Train.query.filter_by(id=train).first().seats
    fee_per_seat = float(fee) / seats + price
    rides = []
    delta = timedelta(weeks=1)
    if rep_type == 'd':
        delta = timedelta(days=1)

    while (start < end):  # as long as there are dates left, add a new ride
        ride = Ride(plannedroute_id,
                    start,
                    fee_per_seat,
                    True,
                    train)
        rides.append(ride)
        start = start + delta

    return rides


# if get request: step two of the form is returned
# if post request: the rides are created with the given information and stored to the db.
def store_ride():
    if request.method == 'POST':
        plannedroute_id = request.form['plannedroute_id']
        rides = []
        if request.form['interval'] == 'False':
            seats = Train.query.filter_by(id=request.form['train']).first().seats
            fee_per_seat = float(request.form['fee']) / seats + float(
                request.form['price'])  # fee per seat plus extra price
            ride = Ride(plannedroute_id,
                        datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M'),
                        fee_per_seat,
                        False,
                        request.form['train'])
            rides.append(ride)
        else:
            rides = create_interval_rides(plannedroute_id,
                                          datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M'),
                                          datetime.strptime(request.form['end'], '%Y-%m-%d'),
                                          request.form['rep_type'],
                                          float(request.form['price']),
                                          request.form['train'],
                                          request.form['fee']
                                          )

        # check, if train is available at this time
        Range = namedtuple('Range', ['start', 'end'])
        all_rides_with_same_train = Ride.query.filter_by(
            train_id=request.form['train']).all()  # get all rides with same train
        for ride in all_rides_with_same_train:
            duration = ride.plannedroute.duration
            start = ride.time
            end = start + timedelta(minutes=duration)
            r1 = Range(start=start, end=end)
            for ride2 in rides:  # for all rides that should be added to the db is checked, if we have an overlapping period of time
                duration2 = PlannedRoute.query.filter_by(id=plannedroute_id).first().duration
                start2 = ride2.time
                end2 = start2 + timedelta(minutes=duration2)
                r2 = Range(start=start2, end=end2)
                latest_start = max(r1.start, r2.start)
                earliest_end = min(r1.end, r2.end)
                delta = (earliest_end - latest_start).days + 1
                overlap = max(0, delta)
                if overlap != 0:
                    flash(
                        "Fahrtdurchführung(en) wurde(n) nicht hinzugefügt. Zug ist zu einem oder mehreren Daten nicht verfügbar")
                    return redirect('/admin')

        for ride in rides:  # add all rides to db. If only a single ride, that list contains one ride.
            employees = [int(e) for e in request.form.getlist('emp')]
            employees = Employee.query.filter(Employee.id.in_(employees)).all()
            ride.executed_by.extend(employees)
            db.session.add(ride)
            db.session.commit()
            flash("Fahrtdurchführung {} wurde hinzugefügt.".format(ride.id))
            db.session.close()
        return redirect('/admin')

    else:
        employees = Employee.query  # all employees can be selected for a ride
        plannedroute_id = request.args['plannedroute_id']
        pr = PlannedRoute.query.filter_by(id=plannedroute_id).first()
        isNormalspur = pr.isNormalspur
        total_fee = pr.fee_sum
        if not isNormalspur:  # only trains, that have the right "Spurgröße" can be selected for the ride.
            trains = Train.query.filter_by(is_normalspur=False)
        else:
            trains = Train.query.all()

        if request.args['interval'] == 'True':  # return form step 2 for interval
            start = request.args['start']
            end = request.args['end']
            rep_type = request.args['rep_type']
            return render_template('admin/plan_interval_ride_step2.html', title='Plan interval ride', start=start,
                                   end=end, rep_type=rep_type,
                                   employees=employees, trains=trains, interval=True, plannedroute_id=plannedroute_id,
                                   fee=total_fee)
        else:  # return form step 2 for single ride
            time = request.args['time']
            return render_template('admin/plan_single_ride_step2.html', title='Plan single ride', time=time,
                                   employees=employees, trains=trains, interval=False, plannedroute_id=plannedroute_id,
                                   fee=total_fee)


# store the route (Fahrtstrecke) that was created in plan_route()
def store_route():
    if request.method == 'POST':
        sections = [int(s) for s in request.form.getlist('sections')]
        sections = Section.query.filter(Section.id.in_(sections)).all()
        start_id = int(request.form['start'])
        end_id = int(request.form['end'])
        # check if sections are connected
        if not is_valid(start_id, end_id, sections):
            flash('Invalide Auswahl...')
            return redirect('/planrouteview')
        start = Station.query.filter_by(id=start_id).first()
        end = Station.query.filter_by(id=end_id).first()
        name = '{}-{}'.format(start.name, end.name)

        pr = PlannedRoute(name, sections, start_id, end_id)
        db.session.add(pr)
        db.session.commit()
        flash("Fahrtstrecke {} wurde hinzugefügt.".format(name))
    return redirect('/admin')


# check if sections selected are connected as well.
def is_valid(start_station_id, end_station_id, sections):
    all_stations = []
    start_end_map = {}
    for s in sections:
        all_stations.extend([s.start_station_id, s.end_station_id])
        start_end_map[s.start_station_id] = s.end_station_id

    if (start_station_id in all_stations) and (end_station_id in all_stations):
        pass
    else:
        return False

    try:
        first = start_station_id
        for x in range(start_end_map.__len__()):
            second = start_end_map[first]
            first = second
    except KeyError as e:
        return False

    return True
