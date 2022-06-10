from flask import Flask, json, flash
import requests, itertools
from urllib.request import urlopen

dummydata = True

def get_rides():
    if dummydata:
        js = open("./dummydata/rides.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5002/plan/get/rides')
        data = json.loads(response.read())
        return data

def get_planned_routes():
    if dummydata:
        js = open("./dummydata/planned_routes.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5002/plan/get/planned_routes')
        data = json.loads(response.read())
        return data

def get_routes():
    if dummydata:
        js = open("./dummydata/routes.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/routes/get')
        data = json.loads(response.read())
        return data
    
def get_sections():
    if dummydata:
        js = open("./dummydata/sections.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/sections/get')
        data = json.loads(response.read())
        return data

def get_trains():
    if dummydata:
        js = open("./dummydata/trains.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/trains')
        data = json.loads(response.read())
        return data

def get_stations():
    if dummydata:
        js = open("./dummydata/stations.json")
        data = json.load(js)
        return data
    else:
        response = urlopen('http://localhost:5003/stations/get')
        data = json.loads(response.read())
        return data

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

def get_route_name():
    routes = get_routes()
    l = []
    for r in routes["routes"]:
        l.append(r["name"])
    return list(dict.fromkeys(l))

def get_route_id_by_name(name):
    routes = get_routes()
    for r in routes["routes"]:
        if r["name"] == name:
            return r["id"]

def get_route_name_by_id(route_id):
    routes = get_routes()
    for r in routes["routes"]:
        if int(r["id"]) == int(route_id):
            return r["name"]

def getStations():
    stations = get_stations()
    list_stations = []
    for s in stations["stations"]:
        list_stations.append(s["name"])
    return list_stations

def getStationsById(id):
    stations = get_stations()
    for s in stations["stations"]:
        if s["id"]==id:
            return s

def getStationsByName(name):
    stations = get_stations()
    for s in stations["stations"]:
        if s["name"]==name:
            return s

def get_sections_by_route_id(id):
    data = get_sections()
    l = []
    for s in data["sections"]:
        if id == s["route"]:
            l.append(s["startStation"])
            l.append(s["endStation"])
    return list(k for k,_ in itertools.groupby(l))

def get_ride_by_id(id):
    data = get_rides()
    for r in data["data"]:
        if id == r["id"]:
            return r

def get_section_by_id(id):
    data = get_sections()
    for s in data["sections"]:
        if id == s["id"]:
            return s

def get_planned_route_by_id(id):
    data = get_planned_routes()
    for pr in data["data"]:
        if int(id) == pr["id"]:
            return pr
        
# def get_section_by_start_station(id, sections):
#     data = get_sections()
#     for s in data["sections"]:
#         if int(id) == s["startStation"] and sections.__contains__(s["id"]):
#             return s

def get_route_of_ride(id):
    planned_route = get_planned_route_by_id(int(id))
    sections_planned_route = list(planned_route["sections"])
    routes = []
    for s in sections_planned_route:
        section = get_section_by_id(s)
        for section_routes in section["routes"]:
            routes.append(section_routes)
    return set(routes)

def get_train_by_id(id):
    data = get_trains()
    for t in data["trains"]:
        if id == t["id"]:
            return t