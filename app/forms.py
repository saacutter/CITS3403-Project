from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username      = StringField('Username or Email Address', validators=[DataRequired()])
    password      = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit        = SubmitField('Log In')

class SignupForm(FlaskForm):
    username         = StringField('Username', validators=[DataRequired()])
    email            = StringField('Email Address', validators=[DataRequired(), Email()])
    password         = PasswordField('Password', validators=[DataRequired()])
<<<<<<< HEAD
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    privacy          = BooleanField('Make Profile Private?')
=======
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
>>>>>>> a1c9758316cbf4658d940029c20ce876bbc30683
    submit           = SubmitField('Sign Up')