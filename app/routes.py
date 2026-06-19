"""Main application routes."""

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page."""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('dashboard.admin'))
        elif current_user.is_teacher():
            return redirect(url_for('dashboard.teacher'))
        else:
            return redirect(url_for('dashboard.student'))
    
    return render_template('index.html')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page."""
    if request.method == 'POST':
        # TODO: Implement contact form handling
        return redirect(url_for('main.home'))
    
    return render_template('contact.html')