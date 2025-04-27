from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialise the Flask server
application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login' # This sets the page that should be rendered when there is a page that requires a log in to view

from app import routes, models