from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import os

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login' # This sets the page that should be rendered when there is a page that requires a log in to view
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

    return application