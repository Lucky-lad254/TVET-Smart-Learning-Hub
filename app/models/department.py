"""Department model for organizing TVET programs."""

from app.extensions import db
from datetime import datetime
from sqlalchemy.orm import validates


class Department(db.Model):
    """Department model for TVET departments.
    
    Examples:
        - Civil Engineering
        - Electrical Engineering
        - ICT
        - Business Studies
    """
    
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False, index=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    courses = db.relationship('Course', backref='department', lazy='dynamic', 
                             cascade='all, delete-orphan')
    
    @validates('code')
    def validate_code(self, key, value):
        """Ensure department code is uppercase."""
        if value:
            return value.upper()
        return value
    
    def __repr__(self):
        return f'<Department {self.code}>'
    
    def __str__(self):
        return self.name
    
    def course_count(self) -> int:
        """Get number of courses in department."""
        return self.courses.count()
    
    def material_count(self) -> int:
        """Get total materials in all courses in this department."""
        return sum(course.material_count() for course in self.courses)
