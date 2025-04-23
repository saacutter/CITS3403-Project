from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Initialise the Flask server
application = Flask(__name__)
application.config.from_object(Config)
application.config["TEMPLATES_AUTO_RELOAD"] = True
db = SQLAlchemy(application)
migrate = Migrate(application, db)

from app import routes, models