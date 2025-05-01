from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

class LoginForm(FlaskForm):
    username      = StringField('Username or Email Address', validators=[DataRequired()])
    password      = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit        = SubmitField('Log In')

class SignupForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired(),Regexp(r'^[a-zA-Z0-9]+$', message="Username must only contain letters and numbers.")])
    email            = StringField('Email Address', validators=[DataRequired(), Email(message="Enter a valid email address.")])
    password         = PasswordField('Password', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]+$', message="Password must be at least 8 characters and contain only letters, numbers, and !@#$%^&*()_+=-")])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message="Passwords must match.")])
    submit           = SubmitField('Sign Up')


