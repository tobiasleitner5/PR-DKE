# flask sqlalchemy

from flask import Flask, render_template, request, jsonify, render_template_string, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
import os

# my classes
import ReadInput

# app.py
# Initialize the Flask application
from sqlalchemy import ForeignKey

app = Flask(__name__)

# sqlite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Bind the instance to the 'app.py' Flask application
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# mockdata
#routes = requests.get('http://localhost:5001/routes')
#sections = requests.get('http://localhost:5001/sections')

class Rides(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    interval = db.Column(db.Boolean)
    interval_number = db.Column(db.Integer)
    sections = db.Column(db.PickleType, nullable=False) #mutable

    def __init__(self, id, route_id, time, price, interval, interval_nr, sections):
        self.time = time
        self.price = price
        self.interval = interval
        self.interval_number = interval_nr
        self.sections = sections
        self.id = id
        self.route_id = route_id

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    mail = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.name,
            'password': self.password
        }

class Crew(db.Model): #table for relationship employee and ride
    __tablename__ = 'crew'
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), primary_key=True)
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)

class Ride_section(db.Model): #table for relationship between ride and section
    __tablename__ = 'ride_sections'
    ride_id = db.Column(db.Integer, ForeignKey('rides.id'), primary_key=True)
    section_id = db.Column(db.Integer, primary_key=True)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

@app.route('/admin/routes')
def get_routes():
    temp = dict(ReadInput.get_routes_mock())['routes']
    print(temp)
    column_names = ['id', 'name']
    return render_template('admin_data_routes_overview.html', records=temp, colnames=column_names, title='Admin Overview - Routes')

@app.route('/admin/sections/<routes_id>')
def get_sections_by_routes(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    print(filtered_sections)
    column_names = ['id', 'route', 'name', 'distance', 'maxSpeed', 'fee']
    return render_template('admin_data_sections_by_route.html', records=filtered_sections, colnames=column_names, title='Admin Overview - Sections')

@app.route('/admin/single/ride/<routes_id>')
def plan_single_ride(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    return render_template('plan_single_ride.html', title='Plan single ride', sections=filtered_sections)

@app.route('/admin/interval/ride/<routes_id>')
def plan_interval_ride(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    return render_template('plan_single_ride.html', title='Plan interval ride for route' + routes_id, sections=filtered_sections)

#@app.route('/admin/ride/store', method='POST')
#def store_ride():

@app.route('/admin/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    colnames = ['id', 'name', 'mail', 'password']
    print({'data': [emp.to_dict() for emp in employees]})
    return render_template('admin_employees.html', colnames=colnames, employees= {'data': [emp.to_dict() for emp in employees]}, title='Employees')

@app.route('/admin/add_employees', methods=['POST', 'GET'])
def add_employee():
    if request.method == 'POST':
        content = request.form
        name = content['name']
        email = content['email']
        password = content['password']
        employee = Employee(name, email, password)

        try:
            db.session.add(employee)
            db.session.commit()
            return redirect('/admin/employees')

        except:
            'There is a problem. Please try again.'

    if request.method == 'GET':
        return render_template('add_employee.html')

@app.route('/admin')
def get_admin():
    return render_template('index_admin.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        employee = Employee.query.filter_by(name=form.username.data).first()
        if employee:
            #if check_password_hash(user.password, form.password.data):
            if (employee.password, form.password.data):
                login_user(employee, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)