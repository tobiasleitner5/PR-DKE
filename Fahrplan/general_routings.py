from flask import Blueprint
from general import index, login

index_blueprint = Blueprint('index_blueprint', __name__, static_folder='static', static_url_path='/static')
index_blueprint.route('/')(index)

login_blueprint = Blueprint('login_blueprint', __name__)
login_blueprint.route('/login', methods=['GET', 'POST'])(login)