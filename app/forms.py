from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FileField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from flask_wtf.file import FileAllowed
from datetime import datetime

class LoginForm(FlaskForm):
    username      = StringField('Username or Email Address', validators=[DataRequired()])
    password      = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit        = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired(),Regexp(r'^[a-zA-Z0-9]+$', message="Username must contain only letters and numbers.")])
    email            = StringField('Email Address', validators=[DataRequired(), Email(message="The email address must be a valid email address")])
    password         = PasswordField('Password', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]+$', message="The password must contain only letters, numbers, and !@#$%^&*()_+=-")])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="The passwords do not match")])
    privacy          = BooleanField('Make my profile private')
    submit           = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    username        = StringField('Username')
    email           = StringField('Email Address')
    password        = PasswordField('Password')
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'webp'])])
    private         = BooleanField('Make my profile private')
    submit          = SubmitField('Save Changes')

class AddTournamentForm(FlaskForm):
    preview = FileField('Add Game Image', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'webp'], "Images only!")])
    name    = StringField('Tournament Name', validators=[DataRequired()])
    game    = StringField('Game', validators=[DataRequired()])
    date    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"type": "date", "max": str(datetime.now().strftime("%Y-%m-%d"))})
    points  = StringField('Points')
    result  = StringField('Result', validators=[DataRequired()])
    submit  = SubmitField('Add Tournament')
