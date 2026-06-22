"""Role model for user authorization.

Defines user roles: Admin, Teacher, Student.
"""

from app.extensions import db
from datetime import datetime


class Role(db.Model):
    """Role model for managing user permissions.
    
    Roles:
        - admin: Full system access
        - teacher: Can upload materials, manage courses
        - student: Can browse and download materials
    """
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    users = db.relationship('User', backref='role', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def create_default_roles():
        """Create default roles if they don't exist."""
        default_roles = [
            {'name': 'admin', 'description': 'System administrator with full access'},
            {'name': 'teacher', 'description': 'Teacher who can upload and manage materials'},
            {'name': 'student', 'description': 'Student who can browse and download materials'}
        ]
        
        for role_data in default_roles:
            if not Role.query.filter_by(name=role_data['name']).first():
                role = Role(
                    name=role_data['name'],
                    description=role_data['description']
                )
                db.session.add(role)
        
        db.session.commit()
