from flask import Flask, json
import requests

dummydata = True


def get_rides():
    if dummydata:
        js = open("./dummydata/rides.json")
        data = json.load(js)
        return data
    else:
        data = requests.get(url="http://localhost:5001/routes/rides")
        return data.json
