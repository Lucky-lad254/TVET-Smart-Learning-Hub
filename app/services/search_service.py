"""Search and material service layer for Phase 3."""

from app.extensions import db
from app.models import Material, SearchIndex
from datetime import datetime
import os


class SearchService:
    """Service layer for search operations.
    
    Handles search indexing, material retrieval, and advanced filtering.
    Integrates with Phase 1-2 models while providing Phase 3 search features.
    """
    
    @staticmethod
    def index_material(material):
        """Index a newly uploaded material.
        
        Called after Material creation in Phase 2 upload process.
        
        Args:
            material: Material object to index
            
        Returns:
            SearchIndex object or None
        """
        if not material.is_published:
            return None
        
        # Check if already indexed
        existing_index = SearchIndex.query.filter_by(material_id=material.id).first()
        if existing_index:
            return SearchIndex.update_index(material)
        
        return SearchIndex.create_index(material)
    
    @staticmethod
    def unindex_material(material_id):
        """Remove material from search index.
        
        Called when material is deleted or unpublished.
        
        Args:
            material_id: ID of material to remove from index
        """
        SearchIndex.delete_index(material_id)
    
    @staticmethod
    def search_materials(query, course_id=None, module_id=None, file_type=None, 
                        page=1, per_page=20):
        """Search materials with optional filters.
        
        Combines full-text search with organizational hierarchy filtering.
        
        Args:
            query: Search query string
            course_id: Filter by course (Phase 1)
            module_id: Filter by module (Phase 1)
            file_type: Filter by file type (Phase 2)
            page: Page number for pagination (1-indexed)
            per_page: Results per page
            
        Returns:
            Dict with 'total', 'page', 'per_page', 'pages', 'results'
        """
        offset = (page - 1) * per_page
        
        filters = {'query': query}
        if course_id:
            filters['course_id'] = course_id
        if module_id:
            filters['module_id'] = module_id
        if file_type:
            filters['file_type'] = file_type
        
        total, results = SearchIndex.search_advanced(filters, limit=per_page, offset=offset)
        
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'results': results
        }
    
    @staticmethod
    def get_course_materials(course_id, page=1, per_page=20):
        """Get all materials for a course with pagination.
        
        Args:
            course_id: Course ID from Phase 1
            page: Page number
            per_page: Results per page
            
        Returns:
            Dict with pagination info and results
        """
        offset = (page - 1) * per_page
        
        total = SearchIndex.query.filter(
            SearchIndex.course_id == course_id,
            SearchIndex.is_indexed == True
        ).count()
        
        results = SearchIndex.query.filter(
            SearchIndex.course_id == course_id,
            SearchIndex.is_indexed == True
        ).order_by(SearchIndex.updated_at.desc()).limit(per_page).offset(offset).all()
        
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'results': results
        }
    
    @staticmethod
    def get_module_materials(module_id, page=1, per_page=20):
        """Get all materials for a module with pagination.
        
        Args:
            module_id: Module ID from Phase 1
            page: Page number
            per_page: Results per page
            
        Returns:
            Dict with pagination info and results
        """
        offset = (page - 1) * per_page
        
        total = SearchIndex.query.filter(
            SearchIndex.module_id == module_id,
            SearchIndex.is_indexed == True
        ).count()
        
        results = SearchIndex.query.filter(
            SearchIndex.module_id == module_id,
            SearchIndex.is_indexed == True
        ).order_by(SearchIndex.updated_at.desc()).limit(per_page).offset(offset).all()
        
        return {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'results': results
        }
    
    @staticmethod
    def get_trending_materials(limit=10):
        """Get trending materials based on recent activity and downloads.
        
        Args:
            limit: Number of materials to return
            
        Returns:
            List of SearchIndex objects with high engagement
        """
        from app.models import Material
        
        # Materials with recent updates and high download count
        return db.session.query(SearchIndex)\
            .join(Material, SearchIndex.material_id == Material.id)\
            .filter(SearchIndex.is_indexed == True)\
            .order_by(
                (Material.download_count.desc() + (
                    db.func.julianday(Material.updated_at) - 
                    db.func.julianday(datetime.utcnow())
                ) * 10).desc()
            ).limit(limit).all()
    
    @staticmethod
    def get_material_by_id(material_id):
        """Get a material with full indexing metadata.
        
        Args:
            material_id: Material ID from Phase 2
            
        Returns:
            Material object with search index info or None
        """
        from app.models import Material
        
        material = Material.query.get(material_id)
        if not material or not material.is_published:
            return None
        
        return material
    
    @staticmethod
    def rebuild_search_index():
        """Rebuild entire search index.
        
        Should be run after migrations or bulk changes.
        Can be called via Flask CLI: flask rebuild-search-index
        
        Returns:
            Dict with rebuild statistics
        """
        print("Rebuilding search index...")
        indexed, skipped, errors = SearchIndex.rebuild_index()
        
        stats = {
            'indexed': indexed,
            'skipped': skipped,
            'errors': errors,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        print(f"Index rebuild complete: {indexed} indexed, {skipped} skipped, {errors} errors")
        return stats


class MaterialService:
    """Service layer for material management.
    
    Handles material operations and keeps search index in sync.
    """
    
    @staticmethod
    def create_material(title, description, filename, filepath, file_type, 
                       file_size, course_id, module_id, uploaded_by_id, is_published=True):
        """Create a new material and index it.
        
        Called from Phase 2 upload endpoints.
        
        Args:
            title: Material title
            description: Material description
            filename: Original filename
            filepath: Full path to uploaded file
            file_type: File extension
            file_size: File size in bytes
            course_id: Course ID (Phase 1)
            module_id: Course ID (Phase 1)
            uploaded_by_id: User ID who uploaded (Phase 1)
            is_published: Whether material is published
            
        Returns:
            Tuple of (Material object, SearchIndex object or None)
        """
        try:
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
            db.session.flush()
            
            # Index if published
            search_index = None
            if is_published:
                search_index = SearchIndex.create_index(material)
            
            db.session.commit()
            return (material, search_index)
        except Exception as e:
            db.session.rollback()
            print(f"Error creating material: {str(e)}")
            return (None, None)
    
    @staticmethod
    def update_material(material_id, **kwargs):
        """Update material and sync search index.
        
        Args:
            material_id: Material ID to update
            **kwargs: Fields to update (title, description, is_published, etc.)
            
        Returns:
            Updated Material object or None
        """
        try:
            material = Material.query.get(material_id)
            if not material:
                return None
            
            # Update material fields
            for key, value in kwargs.items():
                if hasattr(material, key):
                    setattr(material, key, value)
            
            material.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Update search index
            SearchIndex.update_index(material)
            
            return material
        except Exception as e:
            db.session.rollback()
            print(f"Error updating material: {str(e)}")
            return None
    
    @staticmethod
    def delete_material(material_id):
        """Delete material and remove from search index.
        
        Args:
            material_id: Material ID to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            material = Material.query.get(material_id)
            if not material:
                return False
            
            # Remove from search index
            SearchIndex.delete_index(material_id)
            
            # Delete file if it exists
            if os.path.exists(material.filepath):
                os.remove(material.filepath)
            
            # Delete material record
            db.session.delete(material)
            db.session.commit()
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting material: {str(e)}")
            return False
    
    @staticmethod
    def publish_material(material_id):
        """Publish a material and add to search index.
        
        Args:
            material_id: Material ID to publish
            
        Returns:
            SearchIndex object or None
        """
        material = MaterialService.update_material(material_id, is_published=True)
        if material:
            return SearchIndex.create_index(material)
        return None
    
    @staticmethod
    def unpublish_material(material_id):
        """Unpublish a material and remove from search index.
        
        Args:
            material_id: Material ID to unpublish
            
        Returns:
            True if successful, False otherwise
        """
        try:
            material = MaterialService.update_material(material_id, is_published=False)
            if material:
                SearchIndex.delete_index(material_id)
                return True
        except Exception as e:
            print(f"Error unpublishing material: {str(e)}")
        
        return False
