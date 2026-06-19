# TVET Smart Learning Hub (TSLH)

**A production-ready Learning Management System for TVET institutions.**

TSLH helps teachers teach effectively and enables students to learn independently through organized digital resources, intelligent search, assessments, and AI-assisted learning.

---

## 📋 Phase 1: Project Foundation

### Current Features

✅ **User Authentication**
- Secure login/logout with password hashing
- User registration (Teacher & Student roles)
- Role-based access control

✅ **Database**
- SQLite (development) with SQLAlchemy ORM
- User & Role models
- Scalable schema for future phases

✅ **Dashboards**
- Administrator dashboard (user management)
- Teacher dashboard (resource management tools)
- Student dashboard (learning interface)

✅ **Professional UI**
- Responsive design with Bootstrap 5
- Blue & white educational theme
- Mobile-friendly navigation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lucky-lad254/TVET-Smart-Learning-Hub.git
   cd TVET-Smart-Learning-Hub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 👤 Default Test Accounts

After first run, the database auto-creates test accounts:

**Administrator**
- Email: `admin@tvet.edu`
- Password: `admin123`

**Teacher**
- Email: `teacher@tvet.edu`
- Password: `teacher123`

**Student**
- Email: `student@tvet.edu`
- Password: `student123`

⚠️ **Change these passwords immediately in production!**

---

## 📁 Project Structure

```
TVET_Smart_Learning_Hub/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── models.py                # Database models (User, Role)
│   ├── auth.py                  # Authentication logic
│   ├── routes.py                # Main routes
│   ├── forms.py                 # Login & registration forms
│   ├── decorators.py            # Role-based decorators
│   ├── dashboard.py             # Dashboard logic
│   ├── errors.py                # Error handlers
│   │
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Homepage
│   │   ├── login.html           # Login page
│   │   ├── register.html        # Registration page
│   │   ├── admin.html           # Admin dashboard
│   │   ├── teacher.html         # Teacher dashboard
│   │   └── student.html         # Student dashboard
│   │
│   └── static/
│       ├── css/
│       │   └── style.css        # Main stylesheet
│       ├── js/
│       │   └── script.js        # JavaScript functions
│       └── images/
│           └── logo.png         # School logo
│
├── instance/
│   └── tvet.db                  # SQLite database (auto-created)
│
├── uploads/                     # User uploads (Phase 2)
│
├── tests/                       # Unit tests (Phase 8)
│
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # MIT License
```

---

## 🔐 Security Features

✅ Password hashing with Werkzeug
✅ Secure session management
✅ CSRF protection (Flask-WTF)
✅ Login required decorators
✅ Role-based authorization
✅ Input validation on forms
✅ SQL injection protection (SQLAlchemy ORM)

---

## 📚 Database Schema (Phase 1)

### Users Table
```
id (Primary Key)
fullname (String)
email (Unique)
password (Hashed)
role (Admin/Teacher/Student)
created_at (DateTime)
```

### Roles
- **Administrator**: Full system access
- **Teacher**: Manage courses, assignments, grades
- **Student**: Access learning materials, submit assignments

---

## 🛣️ Development Roadmap

- **Phase 1** ✅ Project Foundation (Complete)
- **Phase 2** 📋 Learning Resources (Upload PDFs, DOCX, videos)
- **Phase 3** 📋 Intelligent Search (Full-text search, OCR)
- **Phase 4** 📋 Teaching Tools (Quizzes, assignments, grading)
- **Phase 5** 📋 Student Tools (Progress tracking, submissions)
- **Phase 6** 📋 AI Features (AI tutor, summarizer)
- **Phase 7** 📋 Administration (Analytics, reports)
- **Phase 8** 📋 Production (Tests, Docker, deployment)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 📧 Support

For questions or issues:
- Open a GitHub Issue
- Email: support@tvet-lms.edu

---

## 👨‍💻 Built with

- **Python 3.12**
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **Bootstrap 5** - UI Framework
- **SQLite** - Database

---

**Last Updated:** June 2026
**Status:** Phase 1 - Stable
