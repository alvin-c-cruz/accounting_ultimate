from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app(config_name='default'):
    # Create an instance of Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration settings from the config object
    app.config.from_object(config[config_name])

    # Initialize database with the app
    db.init_app(app)

    # Register blueprints for your routes
    from application.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/')

    migrate = Migrate(app, db)

    return app
