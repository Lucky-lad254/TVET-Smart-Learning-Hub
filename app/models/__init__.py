"""Database models package.

Exports all models for use throughout the application.
"""

from app.models.role import Role
from app.models.user import User
from app.models.department import Department
from app.models.course import Course
from app.models.module import Module
from app.models.material import Material
from app.models.search_index import SearchIndex

__all__ = [
    'Role',
    'User',
    'Department',
    'Course',
    'Module',
    'Material',
    'SearchIndex'
]
