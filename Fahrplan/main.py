# flask sqlalchemy
from flask import Flask
from flask_bootstrap import Bootstrap

import os

# my classes
from Models import db
from admin_routings import get_routes_blueprint, get_sections_by_routes_blueprint, plan_single_ride_blueprint, plan_interval_ride_blueprint, get_employees_blueprint, add_employee_blueprint, get_admin_blueprint
from general_routings import index_blueprint, login_blueprint

app = Flask(__name__)

# sqlite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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

if __name__ == "__main__":
    app.run(debug=True)