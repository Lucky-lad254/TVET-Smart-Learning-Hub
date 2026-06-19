from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """Login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """Registration form for new users."""
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Register as', choices=[
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        """Check if email already exists."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. Please use a different email or login.')

class UpdateProfileForm(FlaskForm):
    """Form to update user profile."""
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    bio = StringField('Bio', validators=[Length(max=500)])
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    """Form to change password."""
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')
