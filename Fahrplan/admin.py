from flask import render_template, request
from werkzeug.utils import redirect

import ReadInput
from Models import Employee, db

def get_routes():
    temp = dict(ReadInput.get_routes_mock())['routes']
    print(temp)
    column_names = ['id', 'name']
    return render_template('admin_data_routes_overview.html', records=temp, colnames=column_names, title='Admin Overview - Routes')

def get_sections_by_routes(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    print(filtered_sections)
    column_names = ['id', 'route', 'name', 'distance', 'maxSpeed', 'fee']
    return render_template('admin_data_sections_by_route.html', records=filtered_sections, colnames=column_names, title='Admin Overview - Sections')

def plan_single_ride(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    return render_template('plan_single_ride.html', title='Plan single ride', sections=filtered_sections)

def plan_interval_ride(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    return render_template('plan_single_ride.html', title='Plan interval ride for route' + routes_id, sections=filtered_sections)

def get_employees():
    employees = Employee.query.all()
    colnames = ['id', 'name', 'mail', 'password']
    print({'data': [emp.to_dict() for emp in employees]})
    return render_template('admin_employees.html', colnames=colnames, employees= {'data': [emp.to_dict() for emp in employees]}, title='Employees')

def add_employee():
    if request.method == 'POST':
        content = request.form
        name = content['name']
        email = content['email']
        password = content['password']
        employee = Employee(name, email, password)

        try:
            db.session.add(employee)
            db.session.commit()
            return redirect('/admin/employees')

        except:
            'There is a problem. Please try again.'

    if request.method == 'GET':
        return render_template('add_employee.html')

def get_admin():
    return render_template('index_admin.html')