"""Flask application factory.

Creates and configures the Flask application.
"""

from flask import Flask
from app.extensions import db, login_manager, csrf, migrate
from app.config import config
import os


def create_app(config_name=None):
    """Create and configure Flask application.
    
    Args:
        config_name: Configuration environment ('development', 'testing', 'production')
                    Defaults to FLASK_ENV or 'development'
    
    Returns:
        Configured Flask application
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Database context
    with app.app_context():
        db.create_all()
    
    return app
