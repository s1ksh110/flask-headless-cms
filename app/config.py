# config.py
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Media upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Flask-Dropzone settings
    DROPZONE_MAX_FILE_SIZE = 16  # In MB
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
    DROPZONE_UPLOAD_MULTIPLE = False
    DROPZONE_UPLOAD_ON_CLICK = True
