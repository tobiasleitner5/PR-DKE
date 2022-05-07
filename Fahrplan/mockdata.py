import json

from flask import Flask

app = Flask(__name__)

@app.route('/routes', methods = ['GET'])
def getRoutes():
    json_file = open('./testdata/routes.json')
    data = json.load(json_file)
    return data

@app.route('/sections', methods = ['GET'])
def getSections():
    json_file = open('./testdata/sections.json')
    data = json.load(json_file)
    return data

@app.route('/trains', methods = ['GET'])
def getTrains():
    json_file = open('./testdata/trains.json')
    data = json.load(json_file)
    return data

if __name__ == "__main__":
    app.run(debug=True, port=5001)