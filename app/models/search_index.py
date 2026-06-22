"""Search index model for full-text search."""

from app.extensions import db
from datetime import datetime


class SearchIndex(db.Model):
    """SearchIndex model for full-text search indexing.
    
    This table stores indexed content from materials for faster searching.
    """
    
    __tablename__ = 'search_index'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False, unique=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # Extracted text from PDF/DOCX
    keywords = db.Column(db.String(1000), nullable=True)  # Comma-separated keywords
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    material = db.relationship('Material', backref='search_index', foreign_keys=[material_id])
    
    def __repr__(self):
        return f'<SearchIndex {self.title}>'
