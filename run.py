"""Application entry point.

Runs the Flask development server.
"""

import os
from app import create_app, db
from app.models import Role, User, Department, Course, Module, Material, SearchIndex

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Register models for Flask shell."""
    return {
        'db': db,
        'Role': Role,
        'User': User,
        'Department': Department,
        'Course': Course,
        'Module': Module,
        'Material': Material,
        'SearchIndex': SearchIndex
    }


@app.before_request
def before_request():
    """Initialize database and default roles."""
    db.create_all()
    Role.create_default_roles()


if __name__ == '__main__':
    app.run(debug=True)
