import json
from urllib.request import urlopen


def get_routes_data():
    response = urlopen('http://localhost:5001/routes')  # Endpoint for routes
    data = json.loads(response.read())
    return data


def get_sections_data():
    response = urlopen('http://localhost:5001/sections')  # Endpoint for sections
    data = json.loads(response.read())
    return data


def get_stations_data():
    response = urlopen('http://localhost:5001/stations')  # Endpoint for stations
    data = json.loads(response.read())
    return data


def get_trains_data():
    response = urlopen('http://localhost:5001/trains')
    data = json.loads(response.read())
    return data
