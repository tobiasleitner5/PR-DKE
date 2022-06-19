from flask import Flask, json, flash
import requests, itertools
from urllib.request import urlopen

# sets either the use of dummydata (True) or the use of data received by the other applications (False)
dummydata = False

# api to retrieve json data of rides
def get_rides():
    if dummydata:
        js = open("./dummydata/rides.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5002/plan/get/rides')
        data = json.loads(response.read())
        return data

# api to retrieve json data of planned routes
def get_planned_routes():
    if dummydata:
        js = open("./dummydata/planned_routes.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5002/plan/get/planned_routes')
        data = json.loads(response.read())
        return data

# api to retrieve json data of all routes
def get_routes():
    if dummydata:
        js = open("./dummydata/routes.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/routes/get')
        data = json.loads(response.read())
        return data

# api to retrieve json data of all sections
def get_sections():
    if dummydata:
        js = open("./dummydata/sections.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/sections/get')
        data = json.loads(response.read())
        return data

# api to retrieve json data of all trains
def get_trains():
    if dummydata:
        js = open("./dummydata/trains.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/trains')
        data = json.loads(response.read())
        return data

# api to retrieve json data of all stations
def get_stations():
    if dummydata:
        js = open("./dummydata/stations.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/stations/get')
        data = json.loads(response.read())
        return data

# api to retrieve json data of warnings
def get_warnings():
    if dummydata:
        js = open("./dummydata/warnings.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/warnings/get')
        data = json.loads(response.read())
        return data

###################################################################################

# returns a list of all route names
def get_route_name():
    routes = get_routes()
    l = []
    for r in routes["routes"]:
        l.append(r["name"])
    return list(dict.fromkeys(l))

# returns the id of one specific route searched for by name
def get_route_id_by_name(name):
    routes = get_routes()
    for r in routes["routes"]:
        if r["name"] == name:
            return r["id"]

# returns the name of one specific route searched for by route id
def get_route_name_by_id(route_id):
    routes = get_routes()
    for r in routes["routes"]:
        if int(r["id"]) == int(route_id):
            return r["name"]

# returns route which includes all sections form parameter list_sections
def get_routeid_by_sections(list_sections):
    routes = get_routes()
    for r in routes["routes"]:
        if all(elem in r["sections"] for elem in list_sections):
            return r

# returns a list of all station names
def getStations():
    stations = get_stations()
    list_stations = []
    for s in stations["stations"]:
        list_stations.append(s["name"])
    return list_stations

# returns a specific station searched for by id
def getStationsById(id):
    stations = get_stations()
    for s in stations["stations"]:
        if s["id"]==id:
            return s

# returns a specific station searched for by name
def getStationsByName(name):
    stations = get_stations()
    for s in stations["stations"]:
        if s["name"]==name:
            return s

# returns all stations of a route
def get_sections_by_route_id(id):
    data = get_sections()
    l = []
    for s in data["sections"]:
        if id == s["route"]:
            l.append(s["startStation"])
            l.append(s["endStation"])
    return list(k for k,_ in itertools.groupby(l))

# returns a specific ride searched for by id
def get_ride_by_id(id):
    data = get_rides()
    for r in data["data"]:
        if id == r["id"]:
            return r

# returns a specific section searched for by id
def get_section_by_id(id):
    data = get_sections()
    for s in data["sections"]:
        if id == s["id"]:
            return s

# returns a specific planned route searched for by id
def get_planned_route_by_id(id):
    data = get_planned_routes()
    for pr in data["data"]:
        if int(id) == pr["id"]:
            return pr

# returns all routes that are part of a planned ride
def get_route_of_ride(id):
    planned_route = get_planned_route_by_id(int(id))
    sections_planned_route = list(planned_route["sections"])
    routes = []
    for s in sections_planned_route:
        section = get_section_by_id(s)
        for section_routes in section["routes"]:
            routes.append(section_routes)
    return set(routes)

# returns a specific train searched for by id
def get_train_by_id(id):
    data = get_trains()
    for t in data["trains"]:
        if id == t["id"]:
            return t