# Database Schema

## Entity Relationship Diagram (ERD)

```
┌─────────────┐
│    roles    │
├─────────────┤
│ id (PK)     │
│ name        │◄──────┐
│ description │      (FK)
│ created_at  │       │
│ updated_at  │       │
└─────────────┘       │
                      │
              ┌───────┴────────┐
              │                │
        ┌─────▼──────────┐     │
        │     users      │     │
        ├────────────────┤     │
        │ id (PK)        │     │
        │ username (UK)  │     │
        │ email (UK)     │     │
        │ password_hash  │     │
        │ first_name     │     │
        │ last_name      │     │
        │ role_id (FK) ──┘     │
        │ is_active      │     │
        │ created_at     │     │
        │ updated_at     │     │
        │ last_login     │     │
        └────────────────┘     │
             │                 │
             │ (FK)            │
             │ uploaded_by_id  │
             │                 │
        ┌────▼──────────────────────────────────┐
        │          materials                   │
        ├────────────────────────────────────────┤
        │ id (PK)                                │
        │ title                                  │
        │ description                            │
        │ filename                               │
        │ filepath (UK)                          │
        │ file_type                              │
        │ file_size                              │
        │ course_id (FK) ─────────┐              │
        │ module_id (FK) ─────┐   │              │
        │ uploaded_by_id (FK)─┤   │              │
        │ is_published       │   │              │
        │ download_count     │   │              │
        │ created_at         │   │              │
        │ updated_at         │   │              │
        └────┬───────────────┼───┼──────────────┘
             │               │   │
             │               │   └────────────────┐
             │               │                    │
             │         ┌─────▼──────────┐         │
             │         │    modules     │         │
             │         ├────────────────┤         │
             │         │ id (PK)        │         │
             │         │ title          │         │
             │         │ description    │         │
             │         │ course_id (FK) │◄────────┘
             │         │ order          │
             │         │ is_active      │
             │         │ created_at     │
             │         │ updated_at     │
             │         └────────────────┘
             │
        ┌────▼──────────────┐
        │     courses       │
        ├───────────────────┤
        │ id (PK)           │
        │ name              │
        │ code (UK)         │
        │ description       │
        │ department_id(FK) │
        │ credit_hours      │
        │ is_active         │
        │ created_at        │
        │ updated_at        │
        └────▲──────────────┘
             │ (FK)
        ┌────┴──────────────┐
        │   departments     │
        ├───────────────────┤
        │ id (PK)           │
        │ name (UK)         │
        │ code (UK)         │
        │ description       │
        │ is_active         │
        │ created_at        │
        │ updated_at        │
        └───────────────────┘

        ┌───────────────────────────┐
        │    search_index           │
        ├───────────────────────────┤
        │ id (PK)                   │
        │ material_id (FK/UK)       │
        │ title                     │
        │ description               │
        │ content (full-text)       │
        │ keywords                  │
        │ course_id (FK)            │
        │ file_type                 │
        │ created_at (indexed)      │
        │ updated_at                │
        └───────────────────────────┘
```

## Table Definitions

### roles

**Purpose**: Define user roles and permissions

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| name | String(50) | UNIQUE, NOT NULL, INDEX | admin, teacher, student |
| description | String(255) | NULL | Role description |
| created_at | DateTime | NOT NULL, DEFAULT(now) | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Indexes**:
- `idx_role_name` on `name`

---

### users

**Purpose**: Store user accounts

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| username | String(80) | UNIQUE, NOT NULL, INDEX | Login username |
| email | String(120) | UNIQUE, NOT NULL, INDEX | Email address |
| password_hash | String(255) | NOT NULL | PBKDF2-SHA256 hash |
| first_name | String(100) | NOT NULL | |
| last_name | String(100) | NOT NULL | |
| role_id | Integer | FK(roles), NOT NULL | User's role |
| is_active | Boolean | NOT NULL, DEFAULT(True) | Account status |
| created_at | DateTime | NOT NULL, DEFAULT(now) | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |
| last_login | DateTime | NULL | Last login time |

**Indexes**:
- `idx_user_username` on `username`
- `idx_user_email` on `email`
- `idx_user_role_id` on `role_id`

**Relationships**:
- FK: `role_id` → `roles.id` (One-to-Many)

---

### departments

**Purpose**: TVET departments

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| name | String(150) | UNIQUE, NOT NULL, INDEX | Civil Engineering, etc. |
| code | String(20) | UNIQUE, NOT NULL, INDEX | CE, EE, etc. |
| description | Text | NULL | Department description |
| is_active | Boolean | NOT NULL, DEFAULT(True) | |
| created_at | DateTime | NOT NULL, DEFAULT(now) | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Indexes**:
- `idx_dept_name` on `name`
- `idx_dept_code` on `code`

---

### courses

**Purpose**: Training courses

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| name | String(200) | NOT NULL, INDEX | Course name |
| code | String(50) | UNIQUE, NOT NULL, INDEX | CT101, PROG102 |
| description | Text | NULL | |
| department_id | Integer | FK(departments), NOT NULL | Parent department |
| credit_hours | Integer | NOT NULL, DEFAULT(3) | |
| is_active | Boolean | NOT NULL, DEFAULT(True) | |
| created_at | DateTime | NOT NULL, DEFAULT(now) | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Constraints**:
- UNIQUE(code, department_id) - Code unique per department

**Indexes**:
- `idx_course_code` on `code`
- `idx_course_dept_id` on `department_id`

---

### modules

**Purpose**: Course topics/chapters

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| title | String(200) | NOT NULL, INDEX | Module title |
| description | Text | NULL | |
| course_id | Integer | FK(courses), NOT NULL | Parent course |
| order | Integer | NOT NULL, DEFAULT(0) | Sequence order |
| is_active | Boolean | NOT NULL, DEFAULT(True) | |
| created_at | DateTime | NOT NULL, DEFAULT(now) | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Indexes**:
- `idx_module_course_id` on `course_id`

---

### materials

**Purpose**: Uploaded learning resources

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| title | String(300) | NOT NULL, INDEX | Material title |
| description | Text | NULL | |
| filename | String(255) | NOT NULL | Original filename |
| filepath | String(500) | UNIQUE, NOT NULL | Storage path |
| file_type | String(20) | NOT NULL | pdf, docx, mp4, etc. |
| file_size | Integer | NOT NULL | Bytes |
| course_id | Integer | FK(courses), NOT NULL | Parent course |
| module_id | Integer | FK(modules), NULL | Parent module (optional) |
| uploaded_by_id | Integer | FK(users), NOT NULL | Uploader |
| is_published | Boolean | NOT NULL, DEFAULT(True) | Visibility |
| download_count | Integer | NOT NULL, DEFAULT(0) | Download counter |
| created_at | DateTime | NOT NULL, DEFAULT(now), INDEX | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Indexes**:
- `idx_material_title` on `title`
- `idx_material_course_id` on `course_id`
- `idx_material_created_at` on `created_at`

**Relationships**:
- FK: `course_id` → `courses.id`
- FK: `module_id` → `modules.id`
- FK: `uploaded_by_id` → `users.id`

---

### search_index

**Purpose**: Full-text search index

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | Integer | PK, Auto-increment | |
| material_id | Integer | FK(materials), UNIQUE, NOT NULL | Material reference |
| title | String(300) | NOT NULL, INDEX | Indexed title |
| description | Text | NULL | Indexed description |
| content | Text | NULL | Extracted PDF/DOCX text |
| keywords | String(1000) | NULL | Comma-separated keywords |
| course_id | Integer | FK(courses), NOT NULL | For filtering |
| file_type | String(20) | NOT NULL | For filtering |
| created_at | DateTime | NOT NULL, DEFAULT(now), INDEX | |
| updated_at | DateTime | NOT NULL, DEFAULT(now) | |

**Indexes**:
- `idx_search_title` on `title`
- `idx_search_created_at` on `created_at`
- Composite: (title, description, keywords) for full-text search

---

## Query Examples

### Find all materials for a course

```sql
SELECT m.* FROM materials m
JOIN courses c ON m.course_id = c.id
WHERE c.id = 1 AND m.is_published = true
ORDER BY m.created_at DESC;
```

### Search materials by keyword

```sql
SELECT m.* FROM materials m
JOIN search_index si ON m.id = si.material_id
WHERE si.title LIKE '%keyword%' 
   OR si.description LIKE '%keyword%'
   OR si.keywords LIKE '%keyword%'
ORDER BY m.created_at DESC
LIMIT 20 OFFSET 0;
```

### Get department with course and module counts

```sql
SELECT 
    d.id, d.name,
    COUNT(DISTINCT c.id) as course_count,
    COUNT(DISTINCT m.id) as material_count
FROM departments d
LEFT JOIN courses c ON d.id = c.department_id
LEFT JOIN materials m ON c.id = m.course_id
WHERE d.is_active = true
GROUP BY d.id, d.name;
```

### Get user's upload history

```sql
SELECT m.id, m.title, m.file_type, m.file_size,
       c.name as course, m.download_count,
       m.created_at
FROM materials m
JOIN courses c ON m.course_id = c.id
WHERE m.uploaded_by_id = ?
ORDER BY m.created_at DESC;
```
