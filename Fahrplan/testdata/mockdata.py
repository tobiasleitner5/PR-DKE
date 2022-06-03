import json

from flask import Flask

app = Flask(__name__)


@app.route('/routes/get', methods=['GET'])
def getRoutes():
    json_file = open('routes.json')
    data = json.load(json_file)
    return data


@app.route('/sections/get', methods=['GET'])
def getSections():
    json_file = open('sections.json')
    data = json.load(json_file)
    return data


@app.route('/trains', methods=['GET'])
def getTrains():
    json_file = open('trains.json')
    data = json.load(json_file)
    return data


@app.route('/stations/get', methods=['GET'])
def getStations():
    json_file = open('stations.json')
    data = json.load(json_file)
    return data


if __name__ == "__main__":
    app.run(debug=True, port=5003)
