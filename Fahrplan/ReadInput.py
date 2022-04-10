import json
from urllib.request import urlopen


def get_routes_mock():
    response = urlopen('http://localhost:5001/routes')
    data = json.loads(response.read())
    return data

def get_sections_mock():
    response = urlopen('http://localhost:5001/sections')
    data = json.loads(response.read())
    return data