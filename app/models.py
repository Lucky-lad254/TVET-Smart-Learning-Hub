"""Database models."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime
from app import db


class Role(db.Model):
    """Role model for RBAC."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='role_obj', lazy=True)
    
    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(64), nullable=False, default='Student')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def check_password(self, password):
        """Check if provided password matches the hashed password."""
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        """Check if user is an admin."""
        return self.role == 'Admin'
    
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.role == 'Teacher'
    
    def is_student(self):
        """Check if user is a student."""
        return self.role == 'Student'
    
    def __repr__(self):
        return f'<User {self.email}>'