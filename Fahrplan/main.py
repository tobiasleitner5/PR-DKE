# flask sqlalchemy
from flask import Flask, redirect, request, url_for, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_admin import Admin

from datetime import datetime

import os
import ast

# my classes
import ReadInput
from models import db, Employee, Ride, Ride_section, Crew
from admin_routings import get_sections_by_routes_blueprint, plan_ride_blueprint
from general_routings import index_blueprint, login_blueprint, logout_blueprint
from views import PlanView, ModelViewWithoutCreate, ModelViewCustom, HomeAdminView

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Admin - in eigene Klasse später
admin = Admin(app, template_mode='bootstrap3', url='/', name='Menü', index_view=HomeAdminView(name='Home'))
admin.add_view(ModelViewCustom(Employee, db.session))
admin.add_view(ModelViewWithoutCreate(Ride, db.session))
admin.add_view(PlanView(name='Plan', endpoint='plan'))

# Blueprints
app.register_blueprint(get_sections_by_routes_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(plan_ride_blueprint)

# Bind the instance to the 'app.py' Flask application
db.init_app(app)
bootstrap = Bootstrap(app)

def create_interval_rides(rep_type, rep, start):
    ride = Ride(request.form['route_id'], datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M'),
                int(request.form['price']), False, None)

    rides = []
    return rides

@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for('login_blueprint.login'))

@app.route('/admin/ride/store', methods=["POST", 'GET'])
def store_ride():
    if request.method == 'POST':
        if request.form['interval'] == 'False':
            ride = Ride(request.form['route_id'], datetime.strptime(request.form['time'], '%Y-%m-%dT%H:%M'),
                        int(request.form['price']), False, None)
            try:
                db.session.add(ride)
                db.session.flush()
                db.session.refresh(ride)
                for s in ast.literal_eval(request.form['sections']):
                    ride_section = Ride_section(ride.id, int(s))
                    db.session.add(ride_section)

                for e in request.form.getlist('emp'):
                    crew = Crew(ride.id, int(e))
                    db.session.add(crew)

                db.session.add(ride)
                db.session.commit()
            except:
                print('There was a problem...')
                return redirect(url_for('/'))
            finally:
                db.session.close()
        else:
            rides = create_interval_rides()
            for ride in rides:
                try:
                    db.session.add(ride)
                    db.session.flush()
                    db.session.refresh(ride)
                    for s in ast.literal_eval(request.form['sections']):
                        ride_section = Ride_section(ride.id, int(s))
                        db.session.add(ride_section)

                    for e in request.form.getlist('emp'):
                        crew = Crew(ride.id, int(e))
                        db.session.add(crew)

                    db.session.add(ride)
                    db.session.commit()
                except:
                    print('There was a problem...')
                    return redirect(url_for('/'))
                finally:
                    db.session.close()

        return 'Ride stored in database.'

    else:  # GET Kann ich noch in admin.py schreiben
        if request.args['interval'] == 'True':
            time = request.args['time']
            route_id = request.args['routes_id']
            sections = request.args.getlist('sections')
            # TODO: Employee Auswahl einschränken
            employees = Employee.query
            trains = dict(ReadInput.get_trains_mock())['trains']
            filtered_trains = []
            for t in trains:
                # TODO: add condition for trains
                filtered_trains.append(t)
            return render_template('admin/plan_interval_ride.html', title='Plan interval ride', time=time,
                                   route_id=route_id, sections=sections, employees=employees, trains=filtered_trains,
                                   routes_id=request.args['routes_id'], interval=True)
        else:
            time = request.args['time']
            route_id = request.args['routes_id']
            sections = request.args.getlist('sections')
            # TODO: Employee Auswahl einschränken
            employees = Employee.query
            trains = dict(ReadInput.get_trains_mock())['trains']
            filtered_trains = []
            for t in trains:
                # TODO: add condition for trains
                filtered_trains.append(t)
            return render_template('admin/plan_single_ride.html', title='Plan single ride', time=time,
                                   route_id=route_id, sections=sections, employees=employees, trains=filtered_trains,
                                   routes_id=request.args['routes_id'], interval=False)

@app.route('/plan/get/rides')
def test():
    return {'data': [reservation.to_dict() for reservation in Ride.query]}

if __name__ == "__main__":
    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    app.run(debug=True)
