"""Dashboard routes for different user roles."""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.decorators import admin_required, teacher_required, student_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/admin')
@login_required
@admin_required
def admin():
    """Admin dashboard."""
    # Get statistics
    total_users = User.query.count()
    total_teachers = User.query.filter_by(role='Teacher').count()
    total_students = User.query.filter_by(role='Student').count()
    active_users = User.query.filter_by(is_active=True).count()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    stats = {
        'total_users': total_users,
        'total_teachers': total_teachers,
        'total_students': total_students,
        'active_users': active_users
    }
    
    return render_template('dashboard/admin.html', stats=stats, recent_users=recent_users)


@dashboard_bp.route('/admin/users')
@login_required
@admin_required
def manage_users():
    """Manage users."""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    
    return render_template('dashboard/manage_users.html', users=users)


@dashboard_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status."""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.email} has been {status}.', 'success')
    
    return redirect(url_for('dashboard.manage_users'))


@dashboard_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('dashboard.manage_users'))
    
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {email} has been deleted.', 'success')
    return redirect(url_for('dashboard.manage_users'))


@dashboard_bp.route('/teacher')
@login_required
@teacher_required
def teacher():
    """Teacher dashboard."""
    return render_template('dashboard/teacher.html')


@dashboard_bp.route('/student')
@login_required
@student_required
def student():
    """Student dashboard."""
    return render_template('dashboard/student.html')


@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('dashboard/profile.html', user=current_user)


@dashboard_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile."""
    data = request.get_json()
    
    current_user.fullname = data.get('fullname', current_user.fullname)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile updated successfully'})