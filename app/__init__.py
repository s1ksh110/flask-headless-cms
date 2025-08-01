# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from .config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()
migrate = Migrate()

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    # Set up login manager
    login_manager.login_view = 'routes.login'  # Redirect to login page if unauthorized

    # Import and register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# Create app instance for interactive use
app = create_app()

# Expose these for easier importing
__all__ = ['app', 'db', 'login_manager', 'admin']
