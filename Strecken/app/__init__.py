from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# source venv/bin/activate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'

if __name__ == '__main__':
    app.run(host='0.0.0.0')

from app import routes, models
