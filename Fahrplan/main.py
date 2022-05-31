from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_admin import Admin

import os
import argparse

from models import db, Employee, Ride
from blueprint_routings import index_blueprint, login_blueprint, logout_blueprint, plan_blueprint, get_rides_blueprint, \
    plan_single_ride_blueprint, plan_route_blueprint, plan_interval_ride_blueprint, store_ride_blueprint, store_route_blueprint, \
    get_plannedroutes_blueprint
from admin import PlanRideView, RideView, EmployeeView, HomeAdminView, PlanRouteView
from reset import reset

# arguments
parser = argparse.ArgumentParser(description='To set reset flag for db.')
parser.add_argument('--reset', help='Set reset to True if you want to reset the db.', type=str)
args = parser.parse_args()

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Admin
admin = Admin(app, template_mode='bootstrap3', url='/', name='Menü', index_view=HomeAdminView(name='Home'))
admin.add_view(EmployeeView(Employee, db.session, 'Mitarbeiter'))
admin.add_view(RideView(Ride, db.session, 'Fahrtdurchführungen'))
admin.add_view(PlanRouteView(name='Fahrtstrecke planen'))
admin.add_view(PlanRideView(name='Fahrtdurchführungen planen'))

# Blueprints
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(plan_single_ride_blueprint)
app.register_blueprint(plan_blueprint)
app.register_blueprint(get_rides_blueprint)
app.register_blueprint(plan_route_blueprint)
app.register_blueprint(plan_interval_ride_blueprint)
app.register_blueprint(store_ride_blueprint)
app.register_blueprint(store_route_blueprint)
app.register_blueprint(get_plannedroutes_blueprint)

# Bind the instance to the 'app.py' Flask application
db.init_app(app)
bootstrap = Bootstrap(app)


if args.reset == 'True':
    if os.path.exists('rides.db'):
        os.remove('rides.db')
    with app.app_context():
        db.create_all()
        reset()


@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for('login_blueprint.login'))


if __name__ == "__main__":
    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))


    app.run(debug=True, port=5002)
