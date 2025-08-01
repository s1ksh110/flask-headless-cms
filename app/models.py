# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    # Define the users table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin role flag

    def set_password(self, password):
        # Hash password for security
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Verify password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'