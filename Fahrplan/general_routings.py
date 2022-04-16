from flask import Blueprint
from general import index, login, logout

index_blueprint = Blueprint('index_blueprint', __name__, static_folder='static', static_url_path='/static')
index_blueprint.route('/')(index)

login_blueprint = Blueprint('login_blueprint', __name__, static_folder='static', static_url_path='/static')
login_blueprint.route('/login', methods=['GET', 'POST'])(login)

logout_blueprint = Blueprint('logout_blueprint', __name__, static_folder='static', static_url_path='/static')
logout_blueprint.route('/logout', methods=['GET'])(logout)