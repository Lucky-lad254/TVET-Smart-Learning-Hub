from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    
    # Configuration
    if os.getenv('FLASK_ENV') == 'production':
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Create database tables
    with app.app_context():
        db.create_all()
        from app.models import User, Role
        
        # Create default roles if they don't exist
        if Role.query.count() == 0:
            admin_role = Role(name='Admin')
            teacher_role = Role(name='Teacher')
            student_role = Role(name='Student')
            db.session.add_all([admin_role, teacher_role, student_role])
            db.session.commit()
        
        # Create test accounts if they don't exist
        if User.query.count() == 0:
            from werkzeug.security import generate_password_hash
            
            admin = User(
                fullname='Administrator',
                email='admin@tvet.edu',
                password=generate_password_hash('admin123'),
                role='Admin'
            )
            teacher = User(
                fullname='Sample Teacher',
                email='teacher@tvet.edu',
                password=generate_password_hash('teacher123'),
                role='Teacher'
            )
            student = User(
                fullname='Sample Student',
                email='student@tvet.edu',
                password=generate_password_hash('student123'),
                role='Student'
            )
            db.session.add_all([admin, teacher, student])
            db.session.commit()
    
    # Register blueprints
    from app.auth import auth_bp
    from app.routes import main_bp
    from app.dashboard import dashboard_bp
    from app.errors import errors_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(errors_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app
