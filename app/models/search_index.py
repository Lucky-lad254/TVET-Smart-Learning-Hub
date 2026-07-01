"""Search index model for full-text search and advanced indexing."""

from app.extensions import db
from datetime import datetime


class SearchIndex(db.Model):
    """SearchIndex model for full-text search indexing.
    
    Phase 3 enhancement: Provides comprehensive full-text search capabilities,
    indexing material metadata and extracted content for fast retrieval.
    
    This table stores indexed content from materials for faster searching
    with support for field-specific queries, filtering, and analytics.
    """
    
    __tablename__ = 'search_index'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), 
                           nullable=False, unique=True, index=True)
    title = db.Column(db.String(300), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # Extracted text from PDF/DOCX
    keywords = db.Column(db.String(1000), nullable=True)  # Comma-separated keywords
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    course_name = db.Column(db.String(200), nullable=True, index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True, index=True)
    module_name = db.Column(db.String(200), nullable=True, index=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    uploaded_by_name = db.Column(db.String(200), nullable=True, index=True)
    file_type = db.Column(db.String(20), nullable=False, index=True)
    file_size = db.Column(db.Integer, nullable=True)  # In bytes
    is_indexed = db.Column(db.Boolean, default=True, nullable=False, index=True)
    index_version = db.Column(db.Integer, default=1, nullable=False)  # For index upgrades
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow, nullable=False, index=True)
    indexed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships (backward compatible with Phase 1-2)
    material = db.relationship('Material', backref='search_index', foreign_keys=[material_id])
    
    def __repr__(self):
        return f'<SearchIndex {self.title}>'
    
    def __str__(self):
        return self.title
    
    # ========== INDEX CREATION & MAINTENANCE ==========
    
    @staticmethod
    def create_index(material):
        """Create a search index entry for a material.
        
        Extracts and indexes all relevant metadata and content from the material.
        Integrates with Phase 1 (User/Course/Module) and Phase 2 (Material Upload).
        
        Args:
            material: Material object to index
            
        Returns:
            SearchIndex object or None if material is not published
        """
        if not material.is_published:
            return None
        
        try:
            # Get related objects from Phase 1-2 data structure
            course = material.course
            module = material.module
            user = material.uploaded_by
            
            index = SearchIndex(
                material_id=material.id,
                title=material.title,
                description=material.description or '',
                course_id=material.course_id,
                course_name=course.name if course else 'Unknown',
                module_id=material.module_id,
                module_name=module.name if module else '',
                uploaded_by_id=material.uploaded_by_id,
                uploaded_by_name=user.get_full_name() if user else 'Unknown',
                file_type=material.file_type,
                file_size=material.file_size,
                keywords=SearchIndex._extract_keywords(material),
                is_indexed=True,
                indexed_at=datetime.utcnow()
            )
            
            db.session.add(index)
            db.session.commit()
            return index
        except Exception as e:
            db.session.rollback()
            print(f"Error creating index for material {material.id}: {str(e)}")
            return None
    
    @staticmethod
    def update_index(material):
        """Update search index for a material.
        
        Synchronizes index with material changes from Phase 2 (Upload/Material updates).
        Handles unpublishing by removing from index.
        
        Args:
            material: Material object to update in index
            
        Returns:
            Updated SearchIndex object or None if unpublished
        """
        index = SearchIndex.query.filter_by(material_id=material.id).first()
        
        if not index:
            return SearchIndex.create_index(material)
        
        if not material.is_published:
            db.session.delete(index)
            db.session.commit()
            return None
        
        try:
            # Update all indexed fields
            course = material.course
            module = material.module
            user = material.uploaded_by
            
            index.title = material.title
            index.description = material.description or ''
            index.course_id = material.course_id
            index.course_name = course.name if course else 'Unknown'
            index.module_id = material.module_id
            index.module_name = module.name if module else ''
            index.uploaded_by_id = material.uploaded_by_id
            index.uploaded_by_name = user.get_full_name() if user else 'Unknown'
            index.file_type = material.file_type
            index.file_size = material.file_size
            index.keywords = SearchIndex._extract_keywords(material)
            index.is_indexed = True
            index.updated_at = datetime.utcnow()
            
            db.session.commit()
            return index
        except Exception as e:
            db.session.rollback()
            print(f"Error updating index for material {material.id}: {str(e)}")
            return None
    
    @staticmethod
    def delete_index(material_id):
        """Delete search index for a material.
        
        Args:
            material_id: ID of material to remove from index
        """
        try:
            index = SearchIndex.query.filter_by(material_id=material_id).first()
            if index:
                db.session.delete(index)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting index for material {material_id}: {str(e)}")
    
    @staticmethod
    def rebuild_index():
        """Rebuild entire search index from all published materials.
        
        Integrates Phase 1-2 data: fetches published materials and re-indexes.
        Should be called periodically or after bulk material changes.
        
        Returns:
            Tuple of (indexed_count, skipped_count, error_count)
        """
        from app.models import Material
        
        try:
            # Clear existing index
            SearchIndex.query.delete()
            db.session.commit()
            
            # Index all published materials from Phase 2
            published_materials = Material.query.filter_by(is_published=True).all()
            indexed_count = 0
            skipped_count = 0
            error_count = 0
            
            for material in published_materials:
                try:
                    if SearchIndex.create_index(material):
                        indexed_count += 1
                    else:
                        skipped_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error indexing material {material.id}: {str(e)}")
                    continue
            
            return (indexed_count, skipped_count, error_count)
        except Exception as e:
            db.session.rollback()
            print(f"Error rebuilding index: {str(e)}")
            return (0, 0, 1)
    
    # ========== SEARCH OPERATIONS ==========
    
    @staticmethod
    def search(query, limit=50, offset=0):
        """Perform full-text search across all indexed materials.
        
        Searches multiple fields: title, description, keywords, course, module, user.
        Case-insensitive ILIKE queries for SQLite/PostgreSQL compatibility.
        
        Args:
            query: Search query string
            limit: Maximum results to return (default 50, max 200)
            offset: Number of results to skip for pagination
            
        Returns:
            Tuple of (total_count, results_list of SearchIndex objects)
        """
        if not query or not query.strip():
            return (0, [])
        
        limit = min(limit, 200)  # Cap at 200 results
        search_term = f'%{query.lower().strip()}%'
        
        try:
            # Build search query - searches all relevant fields
            search_results = SearchIndex.query.filter(
                db.and_(
                    SearchIndex.is_indexed == True,
                    db.or_(
                        SearchIndex.title.ilike(search_term),
                        SearchIndex.description.ilike(search_term),
                        SearchIndex.keywords.ilike(search_term),
                        SearchIndex.course_name.ilike(search_term),
                        SearchIndex.module_name.ilike(search_term),
                        SearchIndex.uploaded_by_name.ilike(search_term),
                    )
                )
            ).order_by(
                SearchIndex.updated_at.desc()
            )
            
            total_count = search_results.count()
            results = search_results.limit(limit).offset(offset).all()
            
            return (total_count, results)
        except Exception as e:
            print(f"Search error: {str(e)}")
            return (0, [])
    
    @staticmethod
    def search_by_field(field_name, query, limit=50, offset=0):
        """Search within a specific field for precise queries.
        
        Supported fields: 'title', 'course', 'module', 'user', 'type', 'keywords'
        
        Args:
            field_name: Field to search in
            query: Search query
            limit: Maximum results
            offset: Results to skip for pagination
            
        Returns:
            Tuple of (total_count, results_list)
        """
        if not query or not query.strip():
            return (0, [])
        
        limit = min(limit, 200)
        search_term = f'%{query.lower().strip()}%'
        
        field_map = {
            'title': SearchIndex.title,
            'course': SearchIndex.course_name,
            'module': SearchIndex.module_name,
            'user': SearchIndex.uploaded_by_name,
            'type': SearchIndex.file_type,
            'keywords': SearchIndex.keywords,
        }
        
        if field_name not in field_map:
            return (0, [])
        
        try:
            search_results = SearchIndex.query.filter(
                db.and_(
                    field_map[field_name].ilike(search_term),
                    SearchIndex.is_indexed == True
                )
            ).order_by(SearchIndex.updated_at.desc())
            
            total_count = search_results.count()
            results = search_results.limit(limit).offset(offset).all()
            
            return (total_count, results)
        except Exception as e:
            print(f"Field search error: {str(e)}")
            return (0, [])
    
    @staticmethod
    def search_advanced(filters, limit=50, offset=0):
        """Advanced search with multiple filter criteria.
        
        Supports filtering by: course, module, file_type, user
        Integrates Phase 1-2 organizational structure (Dept → Course → Module).
        
        Args:
            filters: Dict with optional keys: 'course_id', 'module_id', 
                    'file_type', 'user_id', 'query'
            limit: Maximum results
            offset: Results to skip
            
        Returns:
            Tuple of (total_count, results_list)
        """
        limit = min(limit, 200)
        
        try:
            query = SearchIndex.query.filter(SearchIndex.is_indexed == True)
            
            # Apply optional filters
            if 'query' in filters and filters['query']:
                search_term = f'%{filters["query"].lower().strip()}%'
                query = query.filter(
                    db.or_(
                        SearchIndex.title.ilike(search_term),
                        SearchIndex.description.ilike(search_term),
                        SearchIndex.keywords.ilike(search_term)
                    )
                )
            
            if 'course_id' in filters and filters['course_id']:
                query = query.filter_by(course_id=filters['course_id'])
            
            if 'module_id' in filters and filters['module_id']:
                query = query.filter_by(module_id=filters['module_id'])
            
            if 'file_type' in filters and filters['file_type']:
                query = query.filter_by(file_type=filters['file_type'].lower())
            
            if 'user_id' in filters and filters['user_id']:
                query = query.filter_by(uploaded_by_id=filters['user_id'])
            
            query = query.order_by(SearchIndex.updated_at.desc())
            total_count = query.count()
            results = query.limit(limit).offset(offset).all()
            
            return (total_count, results)
        except Exception as e:
            print(f"Advanced search error: {str(e)}")
            return (0, [])
    
    # ========== BROWSING & ANALYTICS ==========
    
    @staticmethod
    def get_recent_materials(limit=20):
        """Get recently indexed materials.
        
        Uses Phase 2 indexed_at timestamp for recency ranking.
        
        Args:
            limit: Number of materials to return
            
        Returns:
            List of SearchIndex objects
        """
        try:
            return SearchIndex.query.filter_by(is_indexed=True)\
                .order_by(SearchIndex.indexed_at.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            print(f"Error fetching recent materials: {str(e)}")
            return []
    
    @staticmethod
    def get_popular_materials(limit=20):
        """Get most downloaded materials from Phase 2.
        
        Joins with Material to rank by download_count.
        
        Args:
            limit: Number of materials to return
            
        Returns:
            List of SearchIndex objects ordered by popularity
        """
        try:
            from app.models import Material
            
            return db.session.query(SearchIndex)\
                .join(Material, SearchIndex.material_id == Material.id)\
                .filter(SearchIndex.is_indexed == True)\
                .order_by(Material.download_count.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            print(f"Error fetching popular materials: {str(e)}")
            return []
    
    @staticmethod
    def get_by_course(course_id, limit=50):
        """Get all indexed materials for a course (Phase 1 organization).
        
        Args:
            course_id: Course ID from Phase 1 structure
            limit: Maximum results
            
        Returns:
            List of SearchIndex objects
        """
        try:
            return SearchIndex.query.filter(
                SearchIndex.course_id == course_id,
                SearchIndex.is_indexed == True
            ).order_by(SearchIndex.updated_at.desc()).limit(limit).all()
        except Exception as e:
            print(f"Error fetching materials by course: {str(e)}")
            return []
    
    @staticmethod
    def get_by_module(module_id, limit=50):
        """Get all indexed materials for a module (Phase 1 organization).
        
        Args:
            module_id: Module ID from Phase 1 structure
            limit: Maximum results
            
        Returns:
            List of SearchIndex objects
        """
        try:
            return SearchIndex.query.filter(
                SearchIndex.module_id == module_id,
                SearchIndex.is_indexed == True
            ).order_by(SearchIndex.updated_at.desc()).limit(limit).all()
        except Exception as e:
            print(f"Error fetching materials by module: {str(e)}")
            return []
    
    @staticmethod
    def get_by_file_type(file_type, limit=50):
        """Get all indexed materials of a specific file type.
        
        Args:
            file_type: File extension to filter by (from Phase 2)
            limit: Maximum results
            
        Returns:
            List of SearchIndex objects
        """
        try:
            return SearchIndex.query.filter(
                SearchIndex.file_type == file_type.lower(),
                SearchIndex.is_indexed == True
            ).order_by(SearchIndex.updated_at.desc()).limit(limit).all()
        except Exception as e:
            print(f"Error fetching materials by type: {str(e)}")
            return []
    
    @staticmethod
    def get_by_user(user_id, limit=50):
        """Get all materials indexed from a specific user (Phase 1).
        
        Args:
            user_id: User ID (teacher/admin) who uploaded materials
            limit: Maximum results
            
        Returns:
            List of SearchIndex objects
        """
        try:
            return SearchIndex.query.filter(
                SearchIndex.uploaded_by_id == user_id,
                SearchIndex.is_indexed == True
            ).order_by(SearchIndex.updated_at.desc()).limit(limit).all()
        except Exception as e:
            print(f"Error fetching materials by user: {str(e)}")
            return []
    
    # ========== HELPER METHODS ==========
    
    @staticmethod
    def _extract_keywords(material):
        """Extract searchable keywords from material.
        
        Combines: file_type, course_name, module_name, material_title
        Can be extended to parse document content in Phase 3+.
        
        Args:
            material: Material object
            
        Returns:
            Comma-separated string of keywords
        """
        keywords = set()
        
        # Add file type as keyword
        keywords.add(material.file_type.lower())
        
        # Add course and module context
        if material.course:
            keywords.add(material.course.name.lower())
        
        if material.module:
            keywords.add(material.module.name.lower())
        
        # Add title words (single words only, min length 3)
        if material.title:
            words = material.title.lower().split()
            for word in words:
                if len(word) >= 3:
                    keywords.add(word.strip('.,!?;:'))
        
        return ','.join(sorted(keywords))
    
    @staticmethod
    def get_index_stats():
        """Get indexing statistics for monitoring.
        
        Returns:
            Dict with index stats: total_indexed, by_type, by_course, etc.
        """
        try:
            total_indexed = SearchIndex.query.filter_by(is_indexed=True).count()
            total_unindexed = SearchIndex.query.filter_by(is_indexed=False).count()
            
            stats = {
                'total_indexed': total_indexed,
                'total_unindexed': total_unindexed,
                'by_type': {},
                'by_course': {},
                'last_updated': None
            }
            
            # Get distribution by file type
            type_counts = db.session.query(
                SearchIndex.file_type, 
                db.func.count(SearchIndex.id)
            ).filter_by(is_indexed=True).group_by(SearchIndex.file_type).all()
            
            stats['by_type'] = {t[0]: t[1] for t in type_counts}
            
            # Get last update time
            last_update = SearchIndex.query.filter_by(is_indexed=True)\
                .order_by(SearchIndex.updated_at.desc()).first()
            
            if last_update:
                stats['last_updated'] = last_update.updated_at.isoformat()
            
            return stats
        except Exception as e:
            print(f"Error getting index stats: {str(e)}")
            return {}
