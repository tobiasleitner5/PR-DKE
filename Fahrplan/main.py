# flask sqlalchemy

from flask import Flask, render_template, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
import requests
from urllib.request import urlopen
import json

# app.py
# Initialize the Flask application
app = Flask(__name__)

# sqlite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the instance to the 'app.py' Flask application
db = SQLAlchemy(app)

# mockdata
#routes = requests.get('http://localhost:5001/routes')
#sections = requests.get('http://localhost:5001/routes')

def get_routes():
    response = urlopen('http://localhost:5001/routes')
    data = json.loads(response.read())
    return data

class Rides(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    interval = db.Column(db.Boolean)
    interval_number = db.Column(db.Integer)
    sections = db.Column(db.PickleType, nullable=False) #mutable

    def __init__(self, time, price, interval, interval_nr, sections):
        self.time = time
        self.price = price
        self.interval = interval
        self.interval_number = interval_nr
        self.sections = sections

@app.route('/admin/routes')
def data():
    temp = dict(get_routes())['routes']
    columnNames = ['id', 'name']
    return render_template('admin_data.html', records=temp, colnames=columnNames, title='Admin Overview - Routes')

if __name__ == "__main__":
    app.run(debug=True)