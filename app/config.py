import os
from dotenv import load_dotenv

class Config:
    # Load the environment variables from the .env file
    load_dotenv()

    # Set the secret key
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Set the database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "app.db")

    # Ensure templates auto-reload as they are updated
    TEMPLATES_AUTO_RELOAD = True