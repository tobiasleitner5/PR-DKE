from models import db, Employee, Route, Station, Train, Section
import read_input

def reset():
    # add admin user
    db.session.add(Employee('Admin', 'admin@oebb.at', 123456789, True))

    # add all input data
    sections = dict(read_input.get_sections_data())['sections']
    sections = Section.from_json(sections)
    for section in sections:
        db.session.add(section)

    routes = dict(read_input.get_routes_data())['routes']
    routes = Route.from_json(routes)
    for route in routes:
        db.session.add(route)

    stations = dict(read_input.get_stations_data())['stations']
    stations = Station.from_json(stations)
    for station in stations:
        db.session.add(station)


    trains = dict(read_input.get_trains_data())['trains']
    trains = Train.from_json(trains)
    for train in trains:
        db.session.add(train)

    db.session.commit()
