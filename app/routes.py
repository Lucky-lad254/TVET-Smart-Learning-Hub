from flask import Blueprint, render_template, request
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Homepage route."""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

@main_bp.route('/departments')
def departments():
    """Departments page route."""
    departments_list = [
        {'name': 'Civil Engineering', 'icon': '🏗️'},
        {'name': 'Mechanical Engineering', 'icon': '⚙️'},
        {'name': 'Electrical Engineering', 'icon': '⚡'},
        {'name': 'Software Development', 'icon': '💻'},
        {'name': 'Hospitality', 'icon': '🍽️'},
        {'name': 'Business Management', 'icon': '💼'},
        {'name': 'Agriculture', 'icon': '🌾'},
        {'name': 'Fashion Design', 'icon': '👗'},
    ]
    return render_template('departments.html', departments=departments_list)
