"""Custom form validators for material uploads."""

from wtforms.validators import ValidationError
from app.models import Material
import os


class FileAllowed:
    """Validate file extension."""
    
    def __init__(self, extensions, message=None):
        self.extensions = set(ext.lower() for ext in extensions)
        self.message = message
    
    def __call__(self, form, field):
        if not field.data:
            return
        
        filename = field.data.filename
        if '.' not in filename:
            raise ValidationError('Filename must have an extension')
        
        ext = filename.rsplit('.', 1)[1].lower()
        if ext not in self.extensions:
            raise ValidationError(self.message or f'Invalid file extension')


class FileSizeLimit:
    """Validate file size."""
    
    def __init__(self, max_size=100*1024*1024, message=None):
        self.max_size = max_size
        self.message = message
    
    def __call__(self, form, field):
        if not field.data:
            return
        
        field.data.seek(0, os.SEEK_END)
        file_size = field.data.tell()
        field.data.seek(0)
        
        if file_size > self.max_size:
            size_mb = self.max_size / (1024 * 1024)
            raise ValidationError(self.message or f'File size must not exceed {size_mb:.0f} MB')
