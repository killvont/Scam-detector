import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")  # Add a default secret key
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data/scam_detector.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Additional configurations
    FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
    LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
