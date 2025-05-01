from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username      = StringField('Username or Email Address', validators=[DataRequired()])
    password      = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit        = SubmitField('Log In')

class SignupForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired()])
    email            = StringField('Email Address', validators=[DataRequired(), Email()])
    password         = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    privacy          = BooleanField('Make my profile private')
    submit           = SubmitField('Sign Up')

class UploadDataForm(FlaskForm):
    file       = FileField('File Upload', validators=[FileAllowed(['json', 'csv'])])
    game       = StringField('Game')
    points     = StringField('Points')
    time_taken = StringField('Time Taken')
    result     = StringField('Result')
    submit     = SubmitField('Add Game')
