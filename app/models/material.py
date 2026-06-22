"""Material model for learning resources."""

from app.extensions import db
from datetime import datetime
import os
from sqlalchemy.orm import validates


class Material(db.Model):
    """Material model for uploaded learning resources.
    
    Supported file types:
        - PDF (.pdf)
        - Documents (.docx, .doc)
        - Presentations (.pptx, .ppt)
        - Videos (.mp4, .avi, .mkv)
        - Images (.png, .jpg, .jpeg, .gif)
        - Audio (.mp3, .wav, .m4a)
    """
    
    __tablename__ = 'materials'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'pdf', 'docx', 'doc', 'pptx', 'ppt',
        'mp4', 'avi', 'mkv', 'mov',
        'png', 'jpg', 'jpeg', 'gif', 'bmp',
        'mp3', 'wav', 'm4a', 'flac'
    }
    
    # File size limit: 100 MB
    MAX_FILE_SIZE = 100 * 1024 * 1024
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False, unique=True)
    file_type = db.Column(db.String(20), nullable=False)  # Extension
    file_size = db.Column(db.Integer, nullable=False)  # In bytes
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=True, nullable=False)
    download_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Material {self.title}>'
    
    def __str__(self):
        return self.title
    
    @validates('file_type')
    def validate_file_type(self, key, value):
        """Ensure file type is lowercase and valid."""
        if value:
            value = value.lower().lstrip('.')
            if value not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f'File type .{value} is not allowed')
            return value
        return value
    
    @staticmethod
    def is_extension_allowed(filename: str) -> bool:
        """Check if file extension is allowed."""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in Material.ALLOWED_EXTENSIONS
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Extract file extension from filename."""
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()
        return ''
    
    def increment_download_count(self) -> None:
        """Increment download counter."""
        self.download_count += 1
        db.session.commit()
    
    def is_video(self) -> bool:
        return self.file_type in {'mp4', 'avi', 'mkv', 'mov'}
    
    def is_audio(self) -> bool:
        return self.file_type in {'mp3', 'wav', 'm4a', 'flac'}
    
    def is_document(self) -> bool:
        return self.file_type in {'pdf', 'docx', 'doc', 'pptx', 'ppt'}
    
    def is_image(self) -> bool:
        return self.file_type in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    @staticmethod
    def get_materials_by_course(course_id: int, published_only: bool = True):
        """Get materials for a course."""
        query = Material.query.filter_by(course_id=course_id)
        if published_only:
            query = query.filter_by(is_published=True)
        return query.order_by(Material.created_at.desc())
    
    @staticmethod
    def get_materials_by_module(module_id: int, published_only: bool = True):
        """Get materials for a module."""
        query = Material.query.filter_by(module_id=module_id)
        if published_only:
            query = query.filter_by(is_published=True)
        return query.order_by(Material.created_at.desc())
