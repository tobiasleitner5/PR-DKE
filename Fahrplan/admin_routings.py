from flask import Blueprint
from admin import get_routes, get_sections_by_routes, plan_single_ride, get_employees, add_employee, get_admin

get_routes_blueprint = Blueprint('get_admin_routes_blueprint', __name__, static_folder='static', static_url_path='/static')
get_routes_blueprint.route('/admin/routes', methods=['GET'])(get_routes)

get_sections_by_routes_blueprint = Blueprint('get_sections_by_routes_blueprint', __name__)
get_sections_by_routes_blueprint.route('/admin/sections/<routes_id>')(get_sections_by_routes)

plan_single_ride_blueprint = Blueprint('plan_single_ride_blueprint', __name__)
plan_single_ride_blueprint.route('/admin/single/ride/<routes_id>')(plan_single_ride)

plan_interval_ride_blueprint = Blueprint('plan_interval_ride_blueprint', __name__)
plan_interval_ride_blueprint.route('/admin/interval/ride/<routes_id>')(plan_single_ride) #TODO change single to interval and also in admin_data_routes_overview.html

get_employees_blueprint = Blueprint('get_employees_blueprint', __name__)
get_employees_blueprint.route('/admin/employees')(get_employees)

add_employee_blueprint = Blueprint('add_employee_blueprint', __name__)
add_employee_blueprint.route('/admin/add_employees',  methods=['POST', 'GET'])(add_employee)

get_admin_blueprint = Blueprint('get_admin_blueprint', __name__, static_folder='static', static_url_path='/static')
get_admin_blueprint.route('/admin')(get_admin)
