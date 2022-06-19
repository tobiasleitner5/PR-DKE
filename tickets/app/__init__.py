from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from sqlalchemy import event

# standard configurations for Flask application
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
event.listen(db.engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
fa = FontAwesome(app)

login.login_message = "You are not allowed to access the page. Please log in!"

from app import routes, models, errors


#############################################################
# command sequence to add an admin by using the python console
# >>> from app import db
# >>> from app.models import User
# >>> u = User(username='admin', email='admin@example.com')
# >>> u.set_password('admin')
# >>> u.set_access('admin')
# >>> db.session.add(u)
# >>> db.session.commit()


