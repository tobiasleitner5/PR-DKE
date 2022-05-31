from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import render_template, request, redirect, url_for
from datetime import datetime, timedelta

from models import Route, PlannedRoute, Train, Ride, Employee, Section, db, Station


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
    column_labels = dict(plannedroute='Fahrtstrecke', time='Datum und Uhrzeit', price='Preis', interval='Intervall', trains='Zug', executed_by='Mitarbeiter')
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


def plan_single_ride(plannedroute_id):
    if request.method == 'GET':
        return render_template('admin/plan_single_ride_step1.html', plannedroute_id=plannedroute_id)
    else:
        time = request.form['time']
        return redirect(url_for('store_ride_blueprint.store_ride', time=time, interval='False', plannedroute_id=plannedroute_id))


def plan_interval_ride(plannedroute_id):
    if request.method == 'GET':
        return render_template('admin/plan_interval_ride_step1.html', plannedroute_id=plannedroute_id)
    else:
        start = request.form['start']
        end = request.form['end']
        rep_type = request.form['rep_type']
        return redirect(url_for('store_ride_blueprint.store_ride', start=start, end=end, rep_type=rep_type, interval='True',
                                plannedroute_id=plannedroute_id))


def plan_route(route_id):
    if request.method == 'GET':
        route = Route.query.filter_by(id=route_id).first()
        sections = route.sections
        stations = []
        end_stations = []
        for section in sections:
            stations.append(section.start_station)
            end_stations.append(section.end_station)

        for e in end_stations:
            if e not in stations:
                stations.append(e)

        return render_template('admin/plan_route.html', title='Plane Fahrtstrecke für Route {}'.format(route.name),
                               sections=sections, routes_id=route_id, stations=stations)

def create_interval_rides(plannedroute_id, start, end, rep_type, price, train, fee):
    seats = Train.query.filter_by(id=train).first().seats
    fee_per_seat = float(fee) / seats + price
    rides = []
    delta = timedelta(weeks=1)
    if rep_type == 'd':
        delta = timedelta(days=1)

    print(plannedroute_id)

    while (start < end):
        ride = Ride(plannedroute_id,
                    start,
                    fee_per_seat,
                    True,
                    train)
        rides.append(ride)
        start = start + delta

    return rides


def store_ride():
    if request.method == 'POST':
        rides = []
        if request.form['interval'] == 'False':
            seats = Train.query.filter_by(id=request.form['train']).first().seats
            fee_per_seat = float(request.form['fee']) / seats + float(request.form['price'])
            ride = Ride(request.form['plannedroute_id'],
                        datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M'),
                        fee_per_seat,
                        False,
                        request.form['train'])
            rides.append(ride)
        else:
            rides = create_interval_rides(request.form['plannedroute_id'],
                                          datetime.strptime(request.form['start'], '%Y-%m-%dT%H:%M'),
                                          datetime.strptime(request.form['end'], '%Y-%m-%d'),
                                          request.form['rep_type'],
                                          float(request.form['price']),
                                          request.form['train'],
                                          request.form['fee']
                                          )
        for ride in rides:
            employees = [int(e) for e in request.form.getlist('emp')]
            employees = Employee.query.filter(Employee.id.in_(employees)).all()
            ride.executed_by.extend(employees)
            db.session.add(ride)
            db.session.commit()
            db.session.close()

        return redirect('/admin')

    else:
        employees = Employee.query
        plannedroute_id = request.args['plannedroute_id']
        pr = PlannedRoute.query.filter_by(id=plannedroute_id).first()
        section_info = pr.get_sections_info()
        isNormalspur = section_info['isNormalspur']
        total_fee = section_info['fee']
        duration = section_info[
            'time']  # TODO filter train falls in Verwendung --> einfach alle Rides abfragen und Uhrzeit checken
        if not isNormalspur:
            trains = Train.query.filter_by(is_normalspur=False)
        else:
            trains = Train.query.all()

        if request.args['interval'] == 'True':
            start = request.args['start']
            end = request.args['end']
            rep_type = request.args['rep_type']
            return render_template('admin/plan_interval_ride_step2.html', title='Plan interval ride', start=start,
                                   end=end, rep_type=rep_type,
                                   employees=employees, trains=trains, interval=True, plannedroute_id=plannedroute_id,
                                   fee=total_fee)
        else:
            time = request.args['time']
            return render_template('admin/plan_single_ride_step2.html', title='Plan single ride', time=time,
                                   employees=employees, trains=trains, interval=False, plannedroute_id=plannedroute_id,
                                   fee=total_fee)


def store_route():
    if request.method == 'POST':
        sections = [int(s) for s in request.form.getlist('sections')]
        sections = Section.query.filter(Section.id.in_(sections)).all()
        start_id = request.form['start']
        end_id = request.form['end']
        start = Station.query.filter_by(id=start_id).first()
        end = Station.query.filter_by(id=end_id).first()
        name = '{}-{}'.format(start.name, end.name)

        pr = PlannedRoute(name, sections, start_id, end_id)
        db.session.add(pr)
        db.session.commit()

    return redirect('/admin')