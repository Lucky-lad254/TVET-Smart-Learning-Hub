"""Module model for organizing course content."""

from app.extensions import db
from datetime import datetime


class Module(db.Model):
    """Module model for course modules/topics.
    
    Examples:
        - Concrete Mix Design
        - Electrical Safety
        - Database Normalization
    """
    
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    materials = db.relationship('Material', backref='module', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.title}>'
    
    def __str__(self):
        return self.title
    
    def material_count(self) -> int:
        """Get number of materials in module."""
        return self.materials.count()
    
    @staticmethod
    def get_modules_by_course(course_id: int):
        """Get all modules for a course ordered by sequence."""
        return Module.query.filter_by(course_id=course_id).order_by(Module.order).all()
