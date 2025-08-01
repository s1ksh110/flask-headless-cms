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
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'routes.login'

    # Register blueprints
    from .routes import bp as main_bp
    from .api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app

# App instance for interactive shell
app = create_app()
