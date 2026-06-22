"""User model for authentication and authorization."""

from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """User model for system authentication.
    
    Attributes:
        id: Unique user identifier
        username: Unique username
        email: User email address
        password_hash: Hashed password (never store plain text)
        first_name: User's first name
        last_name: User's last name
        role_id: Foreign key to Role
        is_active: Account status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    uploaded_materials = db.relationship('Material', backref='uploaded_by', lazy='dynamic', 
                                        foreign_keys='Material.uploaded_by_id',
                                        cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def set_password(self, password: str) -> None:
        """Hash and set password.
        
        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role.
        
        Args:
            role_name: Name of role to check
            
        Returns:
            True if user has role, False otherwise
        """
        return self.role.name == role_name
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.has_role('admin')
    
    def is_teacher(self) -> bool:
        """Check if user is teacher."""
        return self.has_role('teacher')
    
    def is_student(self) -> bool:
        """Check if user is student."""
        return self.has_role('student')
    
    def get_full_name(self) -> str:
        """Get user's full name."""
        return f'{self.first_name} {self.last_name}'
