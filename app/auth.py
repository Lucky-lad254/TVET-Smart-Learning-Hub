"""Authentication routes."""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db
from app.models import User
from app.forms import LoginForm, RegistrationForm, ChangePasswordForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('Your account has been disabled. Contact administrator.', 'warning')
                    return redirect(url_for('auth.login'))
                
                login_user(user)
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                
                # Redirect based on role
                if user.is_admin():
                    return redirect(url_for('dashboard.admin'))
                elif user.is_teacher():
                    return redirect(url_for('dashboard.teacher'))
                else:
                    return redirect(url_for('dashboard.student'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        
        return render_template('auth/login.html', form=form)
    
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                fullname=form.fullname.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'danger')
        
        return render_template('auth/register.html', form=form)
    
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        from flask_login import current_user
        
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('main.home'))
    
    return render_template('auth/change_password.html', form=form)