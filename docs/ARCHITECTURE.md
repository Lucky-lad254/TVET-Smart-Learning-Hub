# System Architecture

## Overview

The TVET Smart Learning Hub follows a modular, layered architecture designed for scalability, maintainability, and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────┐
│      Client Layer (Browser)         │
│   HTML/CSS/JavaScript/Bootstrap     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Web Server (Flask)             │
│  - Route handling                   │
│  - Request validation               │
│  - Error handling                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Business Logic Layer           │
│  ┌──────────────────────────────┐  │
│  │ Services (File, Material)    │  │
│  │ Validators                   │  │
│  │ Search Engine                │  │
│  └──────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Data Access Layer (ORM)        │
│  ┌──────────────────────────────┐  │
│  │ SQLAlchemy Models:           │  │
│  │ - Role, User, Department     │  │
│  │ - Course, Module, Material   │  │
│  │ - SearchIndex                │  │
│  └──────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Database Layer                 │
│  SQLite (Dev) / PostgreSQL (Prod)   │
└─────────────────────────────────────┘
```

## Component Description

### 1. Models Layer (`app/models/`)

Core database models using SQLAlchemy ORM.

**Models**:
- `Role` - User roles (admin, teacher, student)
- `User` - User accounts with authentication
- `Department` - TVET departments (Civil, Electrical, etc.)
- `Course` - Training courses within departments
- `Module` - Topics/chapters within courses
- `Material` - Uploaded learning resources
- `SearchIndex` - Full-text search index

**Relationships**:
```
Role (1) ──→ (M) User
                  │
                  ├─→ Material (uploaded_by)
                  │
Department (1) ──→ (M) Course (1) ──→ (M) Module (1) ──→ (M) Material
                                                              │
                                              SearchIndex ←──┘
```

### 2. Services Layer (`app/materials/services.py`)

Business logic and file operations.

**Services**:
- `FileUploadService` - Secure file upload/validation
- `MaterialService` - Material CRUD operations

**Key Methods**:
```python
# File operations
FileUploadService.validate_file()      # Validate uploads
FileUploadService.save_file()          # Save to disk
FileUploadService.delete_file()        # Delete from disk
FileUploadService.generate_unique_filename()  # UUID-based naming

# Material operations
MaterialService.create_material()      # Add to database
MaterialService.update_material()      # Update metadata
MaterialService.delete_material()      # Remove material
MaterialService.get_user_materials()   # List user uploads
```

### 3. Routes Layer (`app/materials/routes.py`)

HTTP endpoints for client requests.

**Endpoints**:
```
GET  /materials/upload              - Upload form
POST /materials/upload              - Handle upload
GET  /materials/my-materials        - Teacher's uploads
GET  /materials/browse              - Browse materials
GET  /materials/search?q=keyword    - Search materials
GET  /materials/material/<id>       - View details
GET  /materials/material/<id>/download  - Download file
POST /materials/material/<id>/delete    - Delete material
```

### 4. Templates Layer (`app/templates/`)

HTML templates with Jinja2 templating.

**Key Templates**:
- `upload.html` - Material upload form
- `browse.html` - Material library browser
- `detail.html` - Material details page
- `my_materials.html` - Teacher's dashboard

### 5. Static Assets (`app/static/`)

CSS, JavaScript, and images.

**Structure**:
```
static/
├── css/
│   └── style.css            - Main stylesheet
├── js/
│   ├── upload.js            - Upload form logic
│   └── search.js            - Search functionality
└── images/
    └── logo.png
```

## Data Flow

### Upload Flow

```
1. User submits form
   ↓
2. Flask receives request
   ↓
3. Validate file (extension, size, type)
   ↓
4. Save to disk (UUID filename)
   ↓
5. Create database record
   ↓
6. Create search index entry
   ↓
7. Return success response
```

### Search Flow

```
1. User enters search query
   ↓
2. Query SearchIndex table
   ↓
3. Full-text search on title/description/content
   ↓
4. Filter by department/course/file type
   ↓
5. Sort and paginate results
   ↓
6. Return materials to frontend
```

## Security Architecture

```
┌─────────────────────────────────────┐
│     Request Authentication          │
│  - JWT / Session based              │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Authorization Checks            │
│  - Role-based access control        │
│  - Resource ownership checks        │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Input Validation                │
│  - File extension whitelist         │
│  - File size limits                 │
│  - CSRF tokens                      │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│     Data Sanitization               │
│  - SQL injection prevention         │
│  - XSS protection                   │
│  - Path traversal prevention        │
└──────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling

- Stateless Flask app (can run on multiple servers)
- Load balancer distributes requests
- Redis for session management
- Separate database server

### Vertical Scaling

- Caching layer (Redis)
- Database indexing
- Query optimization
- File compression

### Performance Optimizations

1. **Database**:
   - Indexed searches (title, created_at)
   - Pagination (avoid loading all records)
   - Query optimization with relationships

2. **File Storage**:
   - UUID-based filenames (fast lookup)
   - Directory organization (course_id/)
   - File compression on upload

3. **Search**:
   - Full-text index in SearchIndex table
   - Cached search results
   - Autocomplete suggestions

## Error Handling

```python
# Service methods return (success, data, error)
success, material, error = MaterialService.create_material(...)

if not success:
    flash(error, 'danger')
    return redirect(url_for('materials.upload_material'))
```

## Configuration Management

**Development**:
```python
DEBUG = True
SQLALCHEMY_ECHO = True
SESSION_COOKIE_SECURE = False
```

**Production**:
```python
DEBUG = False
SESSION_COOKIE_SECURE = True
DATABASE_URL = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
```

## Extension Points

Where to add new features:

1. **New Model**: Add to `app/models/`
2. **New Service**: Add to `app/materials/services.py`
3. **New Route**: Add to `app/materials/routes.py`
4. **New Template**: Add to `app/templates/`
5. **New Validator**: Add to `app/materials/validators.py`
