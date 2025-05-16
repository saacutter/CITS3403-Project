from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login' # This sets the page that should be rendered when there is a page that requires a log in to view
moment = Moment() # This is used for converting the time to human readable time

def create_application(config):
    # Initialise the Flask server
    application = Flask(__name__)
    application.config.from_object(config)

    # Configure the routes from the blueprint
    from app.blueprints import blueprint
    application.register_blueprint(blueprint)

    # Initialise the components of the application
    db.init_app(application)
    login.init_app(application)
    moment.init_app(application)

    # Make the necessary directories for storing images on the server if they don't exist
    os.makedirs(application.config['PFP_UPLOAD_PATH'], exist_ok=True) # This is used to create the directory for user profile pictures
    os.makedirs(application.config['TP_UPLOAD_PATH'], exist_ok=True) # This is used to create the directory for tournament previews
    os.makedirs(application.config['LOG_PATH'], exist_ok=True) # This is used to create the directory for log files

    if config.__name__ == "DeploymentConfig":
        # Create the file handler and set it up (adapted from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling)
        file_handler = RotatingFileHandler(application.config['LOG_PATH'] + '/manager.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        application.logger.addHandler(file_handler)
        application.logger.setLevel(logging.INFO)
        application.logger.info('Server startup')

    return application