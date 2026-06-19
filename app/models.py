from app import db
from flask_login import UserMixin
from datetime import datetime

class Role(db.Model):
    """Role model for user permissions."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Admin, Teacher, Student
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    """User model with authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    role = db.Column(db.String(20), nullable=False, default='Student')  # Admin, Teacher, Student
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
    
    def is_admin(self):
        """Check if user is administrator."""
        return self.role == 'Admin'
    
    def is_teacher(self):
        """Check if user is teacher."""
        return self.role == 'Teacher'
    
    def is_student(self):
        """Check if user is student."""
        return self.role == 'Student'
    
    def set_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
