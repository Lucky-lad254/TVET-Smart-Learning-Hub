"""Course model for organizing training programs."""

from app.extensions import db
from datetime import datetime
from sqlalchemy.orm import validates


class Course(db.Model):
    """Course model for TVET courses.
    
    Examples:
        - Concrete Technology
        - Electrical Machines
        - Database Design
    """
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    credit_hours = db.Column(db.Integer, default=3, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    modules = db.relationship('Module', backref='course', lazy='dynamic',
                             cascade='all, delete-orphan')
    materials = db.relationship('Material', backref='course', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('code', 'department_id', name='unique_course_code_per_dept'),
    )
    
    @validates('code')
    def validate_code(self, key, value):
        """Ensure course code is uppercase."""
        if value:
            return value.upper()
        return value
    
    def __repr__(self):
        return f'<Course {self.code}>'
    
    def __str__(self):
        return self.name
    
    def module_count(self) -> int:
        """Get number of modules in course."""
        return self.modules.count()
    
    def material_count(self) -> int:
        """Get total materials in this course."""
        return self.materials.count()
