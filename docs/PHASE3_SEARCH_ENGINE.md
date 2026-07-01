# Phase 3 - Search Engine & Indexing Implementation Guide

## Overview
Phase 3 enhances the TVET Smart Learning Hub with a full-text search engine
and advanced indexing system, seamlessly integrated with Phase 1 (Authentication)
and Phase 2 (Material Upload System).

## Architecture

### Components
1. **SearchIndex Model** (`app/models/search_index.py`)
   - Full-text search indexing for all materials
   - Supports multiple search fields
   - Compatible with SQLite and PostgreSQL

2. **Search Service** (`app/services/search_service.py`)
   - Business logic for search operations
   - Material management service
   - Index maintenance and rebuilding

3. **Search Routes** (`app/search/routes.py`)
   - REST API endpoints for search queries
   - Browse, trending, and popular materials
   - Admin index management

## Database Schema

### search_index Table
```
id                  INTEGER PRIMARY KEY
material_id         INTEGER FOREIGN KEY (materials.id) - UNIQUE
title               VARCHAR(300) - INDEXED
description         TEXT
content             TEXT
keywords            VARCHAR(1000)
course_id           INTEGER FOREIGN KEY (courses.id) - INDEXED
course_name         VARCHAR(200) - INDEXED
module_id           INTEGER FOREIGN KEY (modules.id) - INDEXED
module_name         VARCHAR(200) - INDEXED
uploaded_by_id      INTEGER FOREIGN KEY (users.id) - INDEXED
uploaded_by_name    VARCHAR(200) - INDEXED
file_type           VARCHAR(20) - INDEXED
file_size           INTEGER
is_indexed          BOOLEAN DEFAULT TRUE - INDEXED
index_version       INTEGER DEFAULT 1
created_at          DATETIME - INDEXED
updated_at          DATETIME - INDEXED
indexed_at          DATETIME
```

## Integration with Phase 1 & 2

### Phase 1 Integration (Authentication)
- **Users**: Materials indexed with uploader info from User model
- **Roles**: Search respects user permissions (via flask_login)
- **Departments**: Organizational hierarchy preserved in search

### Phase 2 Integration (Material Upload)
- **Automatic Indexing**: Materials indexed when uploaded
- **Sync on Update**: Index updated when material changes
- **Sync on Delete**: Index entry removed when material deleted
- **Publish/Unpublish**: Control material visibility via is_published

## API Endpoints

### Search Operations
```
GET /search/query?q=keyword&course_id=1&page=1
  Full-text search with optional filters
  Returns: paginated results with metadata

GET /search/browse?course_id=1&page=1
  Browse materials by organizational structure
  
GET /search/field?field=title&q=keyword
  Search within specific fields (title, course, module, user, type)

GET /search/trending?limit=10
  Get trending materials based on activity
  
GET /search/popular?limit=10
  Get most downloaded materials
```

### Admin Operations
```
GET /search/stats
  Get index statistics and system info
  
POST /search/rebuild
  Rebuild entire search index
```

## Usage Examples

### Basic Search
```python
from app.models import SearchIndex

# Full-text search
total, results = SearchIndex.search("Python Programming", limit=50)

# Search with pagination
total, results = SearchIndex.search("Python", limit=20, offset=40)

# Field-specific search
total, results = SearchIndex.search_by_field("course", "Electrical", limit=50)
```

### Advanced Search
```python
filters = {
    'query': 'calculus',
    'course_id': 5,
    'file_type': 'pdf',
    'user_id': 12
}
total, results = SearchIndex.search_advanced(filters, limit=50)
```

## CLI Commands

### Rebuild Search Index
```bash
flask rebuild-search-index
```

### Get Index Statistics
```bash
flask search-stats
```

### Test Search
```bash
flask search-test --query "Python"
```

## Troubleshooting

**Materials not showing in search:**
- Verify material is published (`is_published=True`)
- Check if index entry exists
- Rebuild index: `flask rebuild-search-index`

**Slow search queries:**
- Check database indexes
- Verify query complexity
- Consider pagination
- Use field-specific search when possible

**Index corruption:**
- Rebuild index completely
- Check database integrity
- Review error logs

## Future Enhancements (Phase 4+)

1. **AI-Powered Search**
   - Semantic search using embeddings
   - Query expansion
   - Related materials recommendation

2. **Content Extraction**
   - PDF text extraction
   - Document OCR
   - Image metadata

3. **Advanced Filtering**
   - Date range filters
   - File size ranges
   - Custom metadata fields

4. **Search Analytics**
   - Popular search terms
   - Search performance metrics
   - User search behavior

5. **Autocomplete**
   - Search suggestions
   - Query completion
   - Typo correction

---

**Phase 3 Complete**: Full-text search engine with advanced indexing
**Compatible**: Phase 1 (Auth) & Phase 2 (Upload)
**Next**: Phase 4 (Quizzes & Assignments)
