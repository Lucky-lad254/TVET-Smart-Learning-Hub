"""Forms for user authentication and registration."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    """Login form."""
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    """Registration form."""
    fullname = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=128)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    role = SelectField('Role', choices=[
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        """Check if email is already registered."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered. Please use a different one.')


class ChangePasswordForm(FlaskForm):
    """Change password form."""
    old_password = PasswordField('Current Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')