"""Search endpoints for Phase 3 - Full-text search and discovery."""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import SearchIndex, Material, Course, Module
from app.services.search_service import SearchService, MaterialService
from app.extensions import db

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/query', methods=['GET', 'POST'])
@login_required
def search_query():
    """Full-text search endpoint.
    
    Supports both simple and advanced search with filters.
    
    Query parameters:
        q: Search query (required)
        course_id: Filter by course (optional)
        module_id: Filter by module (optional)
        type: Filter by file type (optional)
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    query = request.args.get('q', '').strip()
    course_id = request.args.get('course_id', type=int)
    module_id = request.args.get('module_id', type=int)
    file_type = request.args.get('type', '').strip().lower()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    per_page = min(per_page, 100)  # Cap at 100 per page
    
    if not query or len(query) < 2:
        return jsonify({
            'error': 'Search query must be at least 2 characters',
            'total': 0,
            'results': []
        }), 400
    
    # Perform search with filters
    results = SearchService.search_materials(
        query=query,
        course_id=course_id,
        module_id=module_id,
        file_type=file_type,
        page=page,
        per_page=per_page
    )
    
    # Convert SearchIndex objects to JSON-serializable dicts
    results['results'] = [
        {
            'id': r.material_id,
            'title': r.title,
            'description': r.description,
            'course_name': r.course_name,
            'module_name': r.module_name,
            'file_type': r.file_type,
            'uploaded_by': r.uploaded_by_name,
            'indexed_at': r.indexed_at.isoformat()
        }
        for r in results['results']
    ]
    
    return jsonify(results)


@search_bp.route('/browse', methods=['GET'])
@login_required
def browse():
    """Browse materials by course or module.
    
    Query parameters:
        course_id: Course to browse (optional)
        module_id: Module to browse (optional)
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    course_id = request.args.get('course_id', type=int)
    module_id = request.args.get('module_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    per_page = min(per_page, 100)
    
    if course_id:
        results = SearchService.get_course_materials(course_id, page, per_page)
        browse_type = 'course'
        browse_name = db.session.query(Course.name).filter_by(id=course_id).scalar() or 'Unknown'
    elif module_id:
        results = SearchService.get_module_materials(module_id, page, per_page)
        browse_type = 'module'
        browse_name = db.session.query(Module.name).filter_by(id=module_id).scalar() or 'Unknown'
    else:
        # Recent materials
        results = {
            'total': SearchIndex.query.filter_by(is_indexed=True).count(),
            'page': page,
            'per_page': per_page,
            'pages': 1,
            'results': SearchIndex.get_recent_materials(limit=per_page)
        }
        browse_type = 'recent'
        browse_name = 'Recent Materials'
    
    # Convert to JSON
    results['results'] = [
        {
            'id': r.material_id,
            'title': r.title,
            'description': r.description,
            'course_name': r.course_name,
            'module_name': r.module_name,
            'file_type': r.file_type,
            'uploaded_by': r.uploaded_by_name,
            'indexed_at': r.indexed_at.isoformat()
        }
        for r in results['results']
    ]
    
    results['browse_type'] = browse_type
    results['browse_name'] = browse_name
    
    return jsonify(results)


@search_bp.route('/trending', methods=['GET'])
def trending():
    """Get trending materials (public endpoint).
    
    Query parameters:
        limit: Number of results (default: 10, max: 50)
    """
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)
    
    materials = SearchService.get_trending_materials(limit)
    
    results = [
        {
            'id': m.material_id,
            'title': m.title,
            'description': m.description,
            'course_name': m.course_name,
            'module_name': m.module_name,
            'file_type': m.file_type,
            'uploaded_by': m.uploaded_by_name,
            'indexed_at': m.indexed_at.isoformat()
        }
        for m in materials
    ]
    
    return jsonify({'trending': results})


@search_bp.route('/popular', methods=['GET'])
def popular():
    """Get most downloaded materials (public endpoint).
    
    Query parameters:
        limit: Number of results (default: 10, max: 50)
    """
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)
    
    materials = SearchIndex.get_popular_materials(limit)
    
    results = [
        {
            'id': m.material_id,
            'title': m.title,
            'description': m.description,
            'course_name': m.course_name,
            'module_name': m.module_name,
            'file_type': m.file_type,
            'uploaded_by': m.uploaded_by_name,
            'indexed_at': m.indexed_at.isoformat()
        }
        for m in materials
    ]
    
    return jsonify({'popular': results})


@search_bp.route('/field', methods=['GET'])
@login_required
def search_field():
    """Search within a specific field.
    
    Query parameters:
        field: Field to search in (title, course, module, user, type, keywords)
        q: Search query
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    field = request.args.get('field', 'title').lower()
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    per_page = min(per_page, 100)
    
    valid_fields = ['title', 'course', 'module', 'user', 'type', 'keywords']
    if field not in valid_fields:
        return jsonify({
            'error': f'Invalid field. Valid fields: {", ".join(valid_fields)}',
            'total': 0,
            'results': []
        }), 400
    
    if not query or len(query) < 2:
        return jsonify({
            'error': 'Search query must be at least 2 characters',
            'total': 0,
            'results': []
        }), 400
    
    offset = (page - 1) * per_page
    total, results = SearchIndex.search_by_field(field, query, limit=per_page, offset=offset)
    
    results_json = [
        {
            'id': r.material_id,
            'title': r.title,
            'description': r.description,
            'course_name': r.course_name,
            'module_name': r.module_name,
            'file_type': r.file_type,
            'uploaded_by': r.uploaded_by_name,
            'indexed_at': r.indexed_at.isoformat()
        }
        for r in results
    ]
    
    return jsonify({
        'field': field,
        'query': query,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'results': results_json
    })


@search_bp.route('/stats', methods=['GET'])
@login_required
def stats():
    """Get search index statistics (admin only).
    
    Returns indexing statistics and system info.
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    stats = SearchIndex.get_index_stats()
    
    return jsonify(stats)


@search_bp.route('/rebuild', methods=['POST'])
@login_required
def rebuild():
    """Rebuild search index (admin only).
    
    Warning: This can take a while with large datasets.
    """
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    rebuild_stats = SearchService.rebuild_search_index()
    
    return jsonify({
        'message': 'Search index rebuild complete',
        'stats': rebuild_stats
    })


@search_bp.route('/material/<int:material_id>', methods=['GET'])
@login_required
def get_material(material_id):
    """Get material details with search metadata.
    
    Args:
        material_id: Material ID
    """
    material = SearchService.get_material_by_id(material_id)
    if not material:
        return jsonify({'error': 'Material not found or not published'}), 404
    
    search_index = SearchIndex.query.filter_by(material_id=material_id).first()
    
    return jsonify({
        'id': material.id,
        'title': material.title,
        'description': material.description,
        'filename': material.filename,
        'file_type': material.file_type,
        'file_size': material.file_size,
        'course_name': search_index.course_name if search_index else '',
        'module_name': search_index.module_name if search_index else '',
        'uploaded_by': search_index.uploaded_by_name if search_index else '',
        'keywords': search_index.keywords if search_index else '',
        'download_count': material.download_count,
        'created_at': material.created_at.isoformat(),
        'updated_at': material.updated_at.isoformat()
    })


def register_search_routes(app):
    """Register search blueprint with Flask app.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(search_bp)
