from app import application, db, migrate, models, forms
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

# Default route of the application
@application.route("/")
@application.route("/index")
def index():
    user = {'username': 'username', 'image': 'https://picsum.photos/200'} # This is just a temporary user where the image is a random image
    return render_template("index.html", user=user) # TODO: signed_out can be assigned to the .is_authenticated method when we come to that

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    # Ensure that the user cannot access this route if they are already signed in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "POST" and forms.LoginForm().validate_on_submit():
        form = forms.LoginForm()

        # Retrieve the user from the database based on the provided username/email address
        user = db.session.scalar(sa.select(models.Users).where((models.Users.username == form.username.data) | (models.Users.email == form.username.data)))

        # Ensure that the user exists and that the password hash matches
        if user is None or not check_password_hash(user.password, form.password.data):
            return redirect(url_for('login'))
        
        # Update the user's last login time and commit it to the database
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # Log the user in and send them to the homepage
        login_user(user, remember=form.remember_user.data)
        return redirect(url_for('index'))
    return render_template("login.html", login=True, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display login page
        
# Signup route of the application
@application.route("/signup", methods=["GET", "POST"])
def signup():
    # Ensure that the user cannot access this route if they are already signed in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == "POST" and forms.SignupForm().validate_on_submit():
        form = forms.SignupForm()

        if form.password.data != form.password_confirm.data:
            return redirect(url_for('login'))
        
        # Hash the password
        password = generate_password_hash(form.password.data)

        # Create the user entry and add it to the database
        user = models.Users(username=form.username.data, password=password, email=form.email.data)
        db.session.add(user)
        db.session.commit()

        # Log in the user and return them to the homepage
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template("login.html", login=False, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display sign up page

@application.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))