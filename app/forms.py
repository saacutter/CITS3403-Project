from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField, FileField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, Regexp, Length, ValidationError
from flask_wtf.file import FileAllowed
from flask_login import current_user
from app import db, models
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image

def is_valid_date(form, field): # Adapted from https://wtforms.readthedocs.io/en/3.0.x/crash_course/#displaying-errors
    today = str(datetime.now().strftime("%Y-%m-%d"))
    if field.data.strftime("%Y-%m-%d") > today:
        raise ValidationError("The tournament cannot be after today's date (" + today + ")")
    
def is_valid_image(form, field):
    # Ensure an image was uploaded
    if not field.data:
        return 
    
    # Save the uploaded image to the server if one was uploaded
    image = field.data
    img_filename = secure_filename(image.filename)
    if img_filename != "":
        # Ensure that the image is roughly square (with a 50px tolerance)
        img = Image.open(image)   
        if abs(img.width - img.height) > 50:
            raise ValidationError("The profile image must be square")
        image.seek(0) # Reset the file point to the start so that it can be saved to the server properly

def is_valid_result(form, field):
    # Check if the result is valid
    if field.data.lower() not in ['win', 'loss', 'draw']:
        raise ValidationError("The result can only be a 'win', 'loss', or 'draw'")

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
    private          = BooleanField('Make my profile private')
    submit           = SubmitField('Sign Up')

    def validate_username(self, field):
        # Check if username already exists
        existing_user = db.session.scalar(sa.select(models.Users).where(sa.func.lower(models.Users.username) == field.data.lower()))
        if existing_user:
            raise ValidationError("A user with this username or email address already exists")
    
    def validate_email(self, field):
        # Check if email is already used
        existing_user = db.session.scalar(sa.select(models.Users).where(models.Users.email == field.data))
        if existing_user:
            raise ValidationError("A user with this username or email address already exists")

class EditProfileForm(FlaskForm):
    username        = StringField('Username', validators=[DataRequired(), Regexp(r'^[a-zA-Z0-9]+$', message="Username must contain only letters and numbers.")])
    email           = StringField('Email Address', validators=[DataRequired(), Email(message="The email address must be a valid email address")])
    password        = PasswordField('Password', validators=[Optional(), Length(min=8, message="The password must be at least 8 characters long"), Regexp(r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]+$', message="The password must contain only letters, numbers, and !@#$%^&*()_+=-")])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpeg', 'jpg', 'png', 'webp', '.svg'], message="The profile image can only be in .png, .jpeg, .svg or .webp format"), is_valid_image])
    private         = BooleanField('Make my profile private')
    submit          = SubmitField('Save Changes')

    def validate_username(self, field):
        # Check if username already exists
        existing_user = db.session.scalar(sa.select(models.Users).where(sa.func.lower(models.Users.username) == field.data.lower()))
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError("A user with this username or email address already exists")
    
    def validate_email(self, field):
        # Check if email is already used
        existing_user = db.session.scalar(sa.select(models.Users).where(models.Users.email == field.data.lower()))
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError("A user with this username or email address already exists")

class AddTournamentForm(FlaskForm):
    preview = FileField('Tournament Preview Image', validators=[Optional(), FileAllowed(['jpeg', 'jpg', 'png', 'webp', '.svg'], message="The profile image can only be in .png, .jpeg, .svg or .webp format"), is_valid_image])
    name    = StringField('Tournament Name', validators=[DataRequired()])
    game    = StringField('Game', validators=[DataRequired()])
    date    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(), is_valid_date], render_kw={"type": "date", "max": str(datetime.now().strftime("%Y-%m-%d"))})
    points  = IntegerField('Points', validators=[DataRequired()])
    result  = StringField('Result', validators=[DataRequired(), is_valid_result])
    details = TextAreaField('Tournament Details', validators=[Optional(), Length(max=64)])
    submit  = SubmitField('Add Tournament')

class EditTournamentForm(FlaskForm):
    preview = FileField('Tournament Preview Image', validators=[Optional(), FileAllowed(['jpeg', 'jpg', 'png', 'webp', 'svg'], message="The profile image can only be in .png, .jpeg, .svg or .webp format"), is_valid_image])
    name    = StringField('Tournament Name', validators=[DataRequired()])
    game    = StringField('Game', validators=[DataRequired()])
    date    = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(), is_valid_date], render_kw={"type": "date", "max": str(datetime.now().strftime("%Y-%m-%d"))})
    points  = IntegerField('Points', validators=[DataRequired()])
    result  = StringField('Result', validators=[DataRequired(), is_valid_result])
    details = TextAreaField('Tournament Details', validators=[Optional(), Length(max=64)])
    submit  = SubmitField('Save Changes')