"""Material upload and file management services.

Handles secure file uploads, validation, and storage.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Material


class FileUploadService:
    """Service for handling secure file uploads."""
    
    ALLOWED_EXTENSIONS = Material.ALLOWED_EXTENSIONS
    MAX_FILE_SIZE = Material.MAX_FILE_SIZE
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate unique filename to prevent collisions."""
        ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        unique_name = f"{uuid.uuid4()}.{ext}" if ext else str(uuid.uuid4())
        return unique_name
    
    @staticmethod
    def validate_file(file, max_size: int = MAX_FILE_SIZE) -> Tuple[bool, str]:
        """Validate uploaded file."""
        if not file or not file.filename:
            return False, "No file selected"
        
        if not FileUploadService.is_extension_allowed(file.filename):
            ext = file.filename.rsplit('.', 1)[1] if '.' in file.filename else 'unknown'
            return False, f"File type .{ext} is not allowed"
        
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size == 0:
            return False, "File is empty"
        
        if file_size > max_size:
            size_mb = max_size / (1024 * 1024)
            return False, f"File size exceeds {size_mb:.0f} MB limit"
        
        return True, ""
    
    @staticmethod
    def is_extension_allowed(filename: str) -> bool:
        """Check if file extension is allowed."""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return ext in FileUploadService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_file(file, upload_folder: str, subfolder: str = None) -> Tuple[bool, str, str]:
        """Save uploaded file to disk."""
        try:
            unique_filename = FileUploadService.generate_unique_filename(file.filename)
            
            if subfolder:
                dir_path = os.path.join(upload_folder, subfolder)
            else:
                dir_path = upload_folder
            
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            filepath = os.path.join(dir_path, unique_filename)
            file.save(filepath)
            
            return True, filepath, ""
            
        except Exception as e:
            return False, "", f"Error saving file: {str(e)}"
    
    @staticmethod
    def delete_file(filepath: str) -> Tuple[bool, str]:
        """Delete file from disk."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True, ""
            return False, "File not found"
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size in bytes."""
        if os.path.exists(filepath):
            return os.path.getsize(filepath)
        return 0


class MaterialService:
    """Service for material database operations."""
    
    @staticmethod
    def create_material(title: str, description: str, filename: str, filepath: str,
                       course_id: int, uploaded_by_id: int, 
                       module_id: int = None, is_published: bool = True) -> Tuple[bool, Material, str]:
        """Create material record in database."""
        try:
            file_type = Material.get_file_extension(filename)
            file_size = FileUploadService.get_file_size(filepath)
            
            material = Material(
                title=title,
                description=description,
                filename=filename,
                filepath=filepath,
                file_type=file_type,
                file_size=file_size,
                course_id=course_id,
                module_id=module_id,
                uploaded_by_id=uploaded_by_id,
                is_published=is_published
            )
            
            db.session.add(material)
            db.session.commit()
            
            return True, material, ""
            
        except Exception as e:
            db.session.rollback()
            return False, None, f"Error creating material: {str(e)}"
    
    @staticmethod
    def delete_material(material_id: int) -> Tuple[bool, str]:
        """Delete material and associated file."""
        try:
            material = Material.query.get(material_id)
            if not material:
                return False, "Material not found"
            
            success, error = FileUploadService.delete_file(material.filepath)
            if not success:
                return False, error
            
            db.session.delete(material)
            db.session.commit()
            
            return True, ""
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting material: {str(e)}"
    
    @staticmethod
    def update_material(material_id: int, **kwargs) -> Tuple[bool, Material, str]:
        """Update material metadata."""
        try:
            material = Material.query.get(material_id)
            if not material:
                return False, None, "Material not found"
            
            allowed_fields = {'title', 'description', 'is_published', 'module_id'}
            for key, value in kwargs.items():
                if key in allowed_fields:
                    setattr(material, key, value)
            
            db.session.commit()
            return True, material, ""
            
        except Exception as e:
            db.session.rollback()
            return False, None, f"Error updating material: {str(e)}"
    
    @staticmethod
    def get_user_materials(user_id: int, course_id: int = None):
        """Get materials uploaded by a user."""
        query = Material.query.filter_by(uploaded_by_id=user_id)
        if course_id:
            query = query.filter_by(course_id=course_id)
        return query.order_by(Material.created_at.desc())
