from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialise the Flask server
application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login' # This sets the page that should be rendered when there is a page that requires a log in to view
moment = Moment(application) # This is used for converting the time to human readable time
os.makedirs(application.config['PFP_UPLOAD_PATH'], exist_ok=True) # This is used to create the directory for user profile pictures
os.makedirs(application.config['TP_UPLOAD_PATH'], exist_ok=True) # This is used to create the directory for tournament previews

# Make a log for keeping a backup of errors (adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling)
os.makedirs(application.config['LOG_PATH'], exist_ok=True)
file_handler = RotatingFileHandler('logs/manager.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
application.logger.addHandler(file_handler)
application.logger.setLevel(logging.INFO)
application.logger.info('Server startup')

from app import routes, models