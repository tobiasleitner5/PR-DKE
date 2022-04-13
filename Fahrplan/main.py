# flask sqlalchemy
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

import os

# my classes
from models import db, Employee
from admin_routings import get_routes_blueprint, get_sections_by_routes_blueprint, plan_single_ride_blueprint, plan_interval_ride_blueprint, get_employees_blueprint, add_employee_blueprint, get_admin_blueprint
from general_routings import index_blueprint, login_blueprint

#login_manager = LoginManager()
#login_manager.login_view = 'login'

def setup_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    # login manager
    #login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(get_routes_blueprint)
    app.register_blueprint(get_sections_by_routes_blueprint)
    app.register_blueprint(get_admin_blueprint)
    app.register_blueprint(plan_single_ride_blueprint)
    app.register_blueprint(plan_interval_ride_blueprint)
    app.register_blueprint(get_employees_blueprint)
    app.register_blueprint(add_employee_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(login_blueprint)

    # Bind the instance to the 'app.py' Flask application
    db.init_app(app)
    bootstrap = Bootstrap(app)
    return app

if __name__ == "__main__":
    setup_app().run(debug=True)
