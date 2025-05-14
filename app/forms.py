from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField, FileField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Regexp, Length
from flask_wtf.file import FileAllowed
from datetime import datetime

class LoginForm(FlaskForm):
    username      = StringField('Username or Email Address', validators=[DataRequired()])
    password      = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit        = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9]+$', message="Username must contain only letters and numbers.")])
    email            = StringField('Email Address', validators=[DataRequired(), Email(message="The email address must be a valid email address")])
    password         = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="The password must be at least 8 characters long"), Regexp(r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]+$', message="The password must contain only letters, numbers, and !@#$%^&*()_+=-")])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="The passwords do not match")])
    privacy          = BooleanField('Make my profile private')
    submit           = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    username        = StringField('Username', validators=[Optional(), Regexp(r'^[a-zA-Z0-9]+$', message="Username must contain only letters and numbers.")])
    email           = StringField('Email Address', validators=[Optional(), Email(message="The email address must be a valid email address")])
    password        = PasswordField('Password', validators=[Optional(), Length(min=8, message="The password must be at least 8 characters long"), Regexp(r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]+$', message="The password must contain only letters, numbers, and !@#$%^&*()_+=-")])
    profile_picture = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpeg', 'jpg', 'png', 'webp'], message="The profile image can only be in .png, .jpeg or .webp format")])
    private         = BooleanField('Make my profile private')
    submit          = SubmitField('Save Changes')

class AddTournamentForm(FlaskForm):
    preview = FileField('Add Game Image', validators=[Optional(), FileAllowed(['jpeg', 'jpg', 'png', 'webp'], message="The profile image can only be in .png, .jpeg or .webp format")])
    name    = StringField('Tournament Name', validators=[DataRequired()])
    game    = StringField('Game', validators=[DataRequired()])
    date    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"type": "date", "max": str(datetime.now().strftime("%Y-%m-%d"))})
    points  = IntegerField('Points', validators=[DataRequired()])
    result  = StringField('Result', validators=[DataRequired()])
    details = TextAreaField('Tournament Details', validators=[Optional()])
    submit  = SubmitField('Add Tournament')
