from flask import Blueprint
from admin import get_sections_by_routes, plan_ride

get_sections_by_routes_blueprint = Blueprint('get_sections_by_routes_blueprint', __name__)
get_sections_by_routes_blueprint.route('/admin/sections/<routes_id>')(get_sections_by_routes)

plan_ride_blueprint = Blueprint('plan_ride_blueprint', __name__)
plan_ride_blueprint.route('/admin/plan/ride/<routes_id>', methods=['GET', 'POST'])(plan_ride)