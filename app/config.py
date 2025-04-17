import os
from dotenv import load_dotenv

class Config:
    # Load the environment variables from the .env file
    load_dotenv()

    # Set the secret key
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Set the database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")