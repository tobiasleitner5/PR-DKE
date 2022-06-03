import json
from urllib.request import urlopen


def get_routes_data():
    response = urlopen('http://localhost:5003/routes/get')  # Endpoint for routes
    data = json.loads(response.read())
    return data


def get_sections_data():
    response = urlopen('http://localhost:5003/sections/get')  # Endpoint for sections
    data = json.loads(response.read())
    return data


def get_stations_data():
    response = urlopen('http://localhost:5003/stations/get')  # Endpoint for stations
    data = json.loads(response.read())
    return data


def get_trains_data():
    response = urlopen('http://localhost:5003/trains')
    data = json.loads(response.read())
    return data
