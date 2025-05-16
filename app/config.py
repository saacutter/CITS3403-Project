import os
from dotenv import load_dotenv

class Config:
    # Load the environment variables from the .env file
    load_dotenv()

    # Set the secret key
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Set the database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

    # Set configuration variables for file uploading
    MAX_CONTENT_LENGTH = 5242880 # Maximum filesize of 5MB
    UPLOAD_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.webp', '.json', '.csv']
    PFP_UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/profilepictures')
    TP_UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/previews')

    # Set configuration variable for log uploading
    LOG_PATH = os.getenv('LOG_PATH') or 'logs'

    # Ensure templates auto-reload as they are updated
    TEMPLATES_AUTO_RELOAD = True