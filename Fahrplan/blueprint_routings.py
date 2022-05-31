from flask import Blueprint
from general import index, login, logout, plan, get_rides, get_planned_routes
from admin import plan_single_ride, plan_route, plan_interval_ride, store_ride, store_route

plan_route_blueprint = Blueprint('plan_route_blueprint', __name__)
plan_route_blueprint.route('/admin/plan/route/<route_id>', methods=['GET'])(plan_route)

plan_single_ride_blueprint = Blueprint('plan_single_ride_blueprint', __name__)
plan_single_ride_blueprint.route('/admin/plan/singleride/<plannedroute_id>', methods=['GET', 'POST'])(plan_single_ride)

plan_interval_ride_blueprint = Blueprint('plan_interval_ride_blueprint', __name__)
plan_interval_ride_blueprint.route('/admin/plan/intervalride/<plannedroute_id>', methods=['GET', 'POST'])(plan_interval_ride)

index_blueprint = Blueprint('index_blueprint', __name__, static_folder='static', static_url_path='/static')
index_blueprint.route('/')(index)

login_blueprint = Blueprint('login_blueprint', __name__, static_folder='static', static_url_path='/static')
login_blueprint.route('/login', methods=['GET', 'POST'])(login)

logout_blueprint = Blueprint('logout_blueprint', __name__, static_folder='static', static_url_path='/static')
logout_blueprint.route('/logout', methods=['GET'])(logout)

plan_blueprint = Blueprint('plan_blueprint', __name__, static_folder='static', static_url_path='/static')
plan_blueprint.route('/planforemployee')(plan)

get_rides_blueprint = Blueprint('get_routes_blueprint', __name__, static_folder='static', static_url_path='/static')
get_rides_blueprint.route('/plan/get/rides')(get_rides)

get_plannedroutes_blueprint = Blueprint('get_plannedroutes_blueprint', __name__, static_folder='static', static_url_path='/static')
get_plannedroutes_blueprint.route('/plan/get/planned_routes')(get_planned_routes)#######

store_ride_blueprint = Blueprint('store_ride_blueprint', __name__, static_folder='static', static_url_path='/static')
store_ride_blueprint.route('/admin/ride/store', methods=['GET', 'POST'])(store_ride)

store_route_blueprint = Blueprint('store_route_blueprint', __name__, static_folder='static', static_url_path='/static')
store_route_blueprint.route('/admin/route/store', methods=['POST'])(store_route)