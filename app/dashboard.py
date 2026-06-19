from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.decorators import admin_required, teacher_required, student_required
from app.models import User
from app import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/admin')
@login_required
@admin_required
def admin():
    """Administrator dashboard."""
    total_users = User.query.count()
    total_teachers = User.query.filter_by(role='Teacher').count()
    total_students = User.query.filter_by(role='Student').count()
    total_admins = User.query.filter_by(role='Admin').count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin.html',
                         total_users=total_users,
                         total_teachers=total_teachers,
                         total_students=total_students,
                         total_admins=total_admins,
                         recent_users=recent_users)

@dashboard_bp.route('/teacher')
@login_required
@teacher_required
def teacher():
    """Teacher dashboard."""
    return render_template('teacher.html', user=current_user)

@dashboard_bp.route('/student')
@login_required
@student_required
def student():
    """Student dashboard."""
    return render_template('student.html', user=current_user)
