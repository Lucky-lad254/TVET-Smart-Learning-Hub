# TVET Smart Learning Hub

**A professional, scalable Python/Flask application for TVET institutions to manage learning materials, student progress, and educational content.**

## Overview

The TVET Smart Learning Hub is designed to help Technical and Vocational Education and Training institutions:

- **Teachers**: Upload, organize, and manage course materials
- **Students**: Browse, search, and download learning resources
- **Administrators**: Manage departments, courses, modules, and monitor usage
- **Data Scientists**: Analyze learning patterns and generate insights

## Features

### ✅ Core Features (Phase 1-2)

- **User Authentication**: Role-based access control (Admin, Teacher, Student)
- **Material Management**: Upload PDFs, documents, videos, audio, images
- **Organization**: Departments → Courses → Modules → Materials
- **Search Engine**: Full-text search, filters, advanced queries
- **File Management**: Secure uploads, virus scanning, compression
- **Download Tracking**: Monitor material popularity and engagement

### 🚀 Upcoming Features (Phase 3+)

- **AI Tutor**: Smart question answering
- **Quiz Generator**: Auto-generated assessments
- **Progress Tracking**: Student learning analytics
- **Mobile App**: iOS/Android support
- **Video Streaming**: Adaptive bitrate delivery
- **Analytics Dashboard**: Usage statistics and insights

## Tech Stack

- **Backend**: Python 3.11+, Flask 2.3
- **Database**: SQLAlchemy ORM, SQLite (dev), PostgreSQL (prod)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Search**: Full-text indexing
- **Deployment**: Docker, AWS, Heroku-ready
- **Testing**: Pytest, coverage reporting

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Lucky-lad25/TVET-Smart-Learning-Hub.git
cd TVET-Smart-Learning-Hub
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Initialize Database

```bash
python run.py
```

Then in Flask shell:

```bash
flask shell
>>> from app.models import Role
>>> Role.create_default_roles()
>>> exit()
```

### 6. Run Application

```bash
python run.py
```

Visit: **http://localhost:5000**

## Project Structure

```
TVET_Smart_Learning_Hub/
├── app/
│   ├── __init__.py              # Flask factory
│   ├── config.py                # Configuration
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── role.py
│   │   ├── user.py
│   │   ├── department.py
│   │   ├── course.py
│   │   ├── module.py
│   │   ├── material.py
│   │   └── search_index.py
│   ├── materials/               # Upload & search
│   │   ├── __init__.py
│   │   ├── services.py
│   │   └── validators.py
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
├── uploads/                     # User uploads
├── tests/                       # Unit tests
├── docs/                        # Documentation
├── run.py                       # Entry point
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── .env.example                 # Environment template
```

## Documentation

Detailed documentation is available in the `docs/` folder:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design & components
- **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - How to extend the app
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - How to use the app
- **[DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - ER diagram & tables
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API endpoints
- **[INSTALLATION.md](docs/INSTALLATION.md)** - Detailed setup guide

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| 1 | Authentication & Foundation | ✅ Complete |
| 2 | Materials & Upload System | ✅ Complete |
| 3 | Search Engine & Indexing | ✅ Complete |
| 4 | Quizzes & Assignments | 🚧 In Progress |
| 5 | AI Integration | Planned |
| 6 | Analytics & Reports | Planned |
| 7 | Mobile Optimization | Planned |
| 8 | Production Release | Planned |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py -v
```

## Deployment

### Docker

```bash
docker build -t tvet-hub .
docker run -p 5000:5000 tvet-hub
```

### Heroku

```bash
heroku create your-app-name
git push heroku main
```

### AWS

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed AWS setup.

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Materials
- `POST /materials/upload` - Upload material
- `GET /materials/browse` - Browse materials
- `GET /materials/search?q=keyword` - Search materials
- `GET /materials/material/<id>` - View details
- `GET /materials/material/<id>/download` - Download file

### Admin
- `POST /admin/departments` - Create department
- `POST /admin/courses` - Create course
- `POST /admin/modules` - Create module

## Security

✅ Password hashing (PBKDF2-SHA256)  
✅ CSRF protection  
✅ SQL injection prevention (SQLAlchemy)  
✅ XSS protection (Jinja2 escaping)  
✅ File type validation  
✅ File size limits (100 MB)  
✅ Role-based authorization  
✅ Secure session management  

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

## Support

For support, issues, or questions:

- Create an [Issue](https://github.com/Lucky-lad25/TVET-Smart-Learning-Hub/issues)
- Check [Discussions](https://github.com/Lucky-lad25/TVET-Smart-Learning-Hub/discussions)
- Email: support@tvet-hub.example.com

## Acknowledgments

Built with ❤️ for TVET institutions worldwide.

---

**Last Updated**: June 2026  
**Version**: 2.0.0-beta
