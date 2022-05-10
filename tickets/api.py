from flask import Flask, json
import requests, itertools

dummydata = True

def get_rides():
    if dummydata:
        js = open("./dummydata/rides.json")
        data = json.load(js)
        return data
    else:
        data = requests.get(url="http://localhost:5001/routes/rides")
        return data.json

def get_routes():
    if dummydata:
        js = open("./dummydata/routes.json")
        data = json.load(js)
        return data
    else:
        data = requests.get(url="http://localhost:5001/routes")
        return data.json
    
def get_sections():
    if dummydata:
        js = open("./dummydata/sections.json")
        data = json.load(js)
        return data
    else:
        data = requests.get(url="http://localhost:5001/sections")
        return data.json

def get_trains():
    if dummydata:
        js = open("./dummydata/trains.json")
        data = json.load(js)
        return data
    else:
        data = requests.get(url="http://localhost:5001/trains")
        return data.json



def getStartStations():
    sections = get_sections()
    l = []
    for s in sections["sections"]:
        l.append(s["startStation"]["name"])
    return list(dict.fromkeys(l))

def getEndStations():
    sections = get_sections()
    l = []
    for s in sections["sections"]:
        l.append(s["endStation"]["name"])
    return list(dict.fromkeys(l))

def get_sections_by_route_id(id):
    data = get_sections()
    l = []
    for s in data["sections"]:
        if id == s["route"]:
            l.append(s["startStation"])
            l.append(s["endStation"])
    return list(k for k,_ in itertools.groupby(l))