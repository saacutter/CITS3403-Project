import os
from dotenv import load_dotenv

class Config:
    # Load the environment variables from the .env file
    load_dotenv()
   
    # Set the secret key
    SECRET_KEY = os.environ['SECRET_KEY']

    # Set configuration variables for file uploading
    MAX_CONTENT_LENGTH = (1024 * 1024)*3 # Maximum filesize of 3MB
    UPLOAD_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp', '.svg', '.json', '.csv']
    PFP_UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profilepictures')
    TP_UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/previews')

    # Set configuration variable for log uploading
    LOG_PATH = os.getenv('LOG_PATH') or 'logs'

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True