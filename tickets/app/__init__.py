from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from sqlalchemy import event

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
fa = FontAwesome(app)

from app import routes, models, errors
