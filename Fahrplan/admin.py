from flask import render_template, request, redirect, url_for

import ReadInput

def get_sections_by_routes(routes_id):
    temp = dict(ReadInput.get_sections_mock())['sections']
    filtered_sections = []
    for section in temp:
        if section['route'] == int(routes_id):
            filtered_sections.append(section)
    column_names = ['id', 'route', 'name', 'distance', 'maxSpeed', 'fee']
    return render_template('admin/admin_data_sections_by_route.html', records=filtered_sections, colnames=column_names, title='Admin Overview - Sections')

def plan_ride(routes_id):
    if request.method == 'GET':
        temp = dict(ReadInput.get_sections_mock())['sections']
        filtered_sections = []
        for section in temp:
            if section['route'] == int(routes_id):
                filtered_sections.append(section)
        return render_template('admin/plan_ride.html', title='Plan ride for route' + routes_id,
                                       sections=filtered_sections, routes_id=routes_id)
    else:
        sections = request.form.getlist('sections')
        time = request.form['time']
        routes_id = request.form['routes_id']
        interval = 'is_interval' in request.form
        return redirect(url_for('store_ride', sections=sections, time=time, routes_id=routes_id, interval=interval))