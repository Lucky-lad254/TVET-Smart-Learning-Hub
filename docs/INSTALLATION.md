# Installation Guide

## System Requirements

- Python 3.11 or higher
- pip (Python package manager)
- Git
- 2GB free disk space
- Modern web browser

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Lucky-lad25/TVET-Smart-Learning-Hub.git
cd TVET-Smart-Learning-Hub
```

### 2. Create Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy environment template:
```bash
cp .env.example .env
```

Edit `.env` file:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/tvet.db
UPLOAD_FOLDER=uploads
```

### 5. Initialize Database

Create directories:
```bash
mkdir -p instance uploads
```

Initialize Flask:
```bash
python run.py
```

In another terminal, create default roles:
```bash
flask shell
```

Inside Flask shell:
```python
from app.models import Role
Role.create_default_roles()
exit()
```

### 6. Run Application

```bash
python run.py
```

Visit: **http://localhost:5000**

## Create Test Accounts

Inside Flask shell:

```python
from app.models import Role, User, Department, Course, Module
from app import db

# Get roles
admin_role = Role.query.filter_by(name='admin').first()
teacher_role = Role.query.filter_by(name='teacher').first()
student_role = Role.query.filter_by(name='student').first()

# Create admin
admin = User(
    username='admin',
    email='admin@school.com',
    first_name='Admin',
    last_name='User',
    role_id=admin_role.id
)
admin.set_password('admin123')
db.session.add(admin)

# Create teacher
teacher = User(
    username='teacher',
    email='teacher@school.com',
    first_name='John',
    last_name='Doe',
    role_id=teacher_role.id
)
teacher.set_password('teacher123')
db.session.add(teacher)

# Create student
student = User(
    username='student',
    email='student@school.com',
    first_name='Jane',
    last_name='Smith',
    role_id=student_role.id
)
student.set_password('student123')
db.session.add(student)

db.session.commit()
print("Test accounts created!")

# Create sample department
dept = Department(
    name='Civil Engineering',
    code='CE',
    description='Civil Engineering Programs'
)
db.session.add(dept)
db.session.commit()

# Create sample course
course = Course(
    name='Concrete Technology',
    code='CT101',
    department_id=dept.id
)
db.session.add(course)
db.session.commit()

# Create sample module
module = Module(
    title='Concrete Mix Design',
    course_id=course.id,
    order=1
)
db.session.add(module)
db.session.commit()

print("Sample data created!")
exit()
```

**Test Credentials**:
- Admin: `admin` / `admin123`
- Teacher: `teacher` / `teacher123`
- Student: `student` / `student123`

## Troubleshooting

### Issue: "No module named 'app'"

**Solution**: Ensure you're in the correct directory:
```bash
cd TVET-Smart-Learning-Hub
```

### Issue: "pip: command not found"

**Solution**: Install pip or use python -m:
```bash
python -m pip install -r requirements.txt
```

### Issue: Database locked

**Solution**: Delete the database and reinitialize:
```bash
rm instance/tvet.db
python run.py
```

### Issue: Port 5000 already in use

**Solution**: Use a different port:
```bash
python run.py --port 5001
```

## Next Steps

1. Login to the application
2. Upload sample materials
3. Browse and search materials
4. Read [USER_GUIDE.md](USER_GUIDE.md) for usage
5. Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) to extend the app
