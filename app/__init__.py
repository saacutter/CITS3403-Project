from flask import Flask
import os
from dotenv import load_dotenv

# Initialise the Flask server
application = Flask(__name__)

# Set the secret key for forms
load_dotenv()
application.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

import app.routes