# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SQLite database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # Disable SQLAlchemy event system to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False