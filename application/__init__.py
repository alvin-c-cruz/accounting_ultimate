from flask import Flask, render_template
from instance.config import config
from flask_migrate import Migrate
from flask_login import login_required

from .extensions import db

from . import blueprints

# Initialize the SQLAlchemy object


def create_app(config_name='default'):
    # Create an instance of Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration settings from the config object
    app.config.from_object(config[config_name])

    # Initialize database with the app
    db.init_app(app)
        
    # Register blueprints for your routes
    module_names = [
        "main",
        "users"
    ]
    
    for module_name in module_names:
        app.register_blueprint(getattr(blueprints, module_name).bp)

    migrate = Migrate(app, db)

    return app
