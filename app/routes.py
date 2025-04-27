from app import application, db, models, forms
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, time

# Default route of the application
@application.route("/")
@application.route("/index")
def index():
    return render_template("index.html")

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

@application.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST" and forms.UploadDataForm().validate_on_submit():
        form = forms.UploadDataForm()

        # Extract the information from the request
        file = request.files['file']
        game = form.game.data
        points = form.points.data
        time_taken = form.time_taken.data
        result = form.result.data

        # Ensure that valid data was provided
        if file == None or (game == "" and points == "" and time_taken == "" and result == ""):
            return redirect(url_for('upload'))

        if file:
            # TODO: Process the file (requires the format of file to be specified)
            ...
        else:
            # Create the tournament entry and add it to the database
            data_entry = models.Tournaments(user_id=current_user.id, game=game, points=points, time_taken=time(0), result=result)
            db.session.add(data_entry)
            db.session.commit()

        return redirect(url_for('index'))
    return render_template("data.html", form=forms.UploadDataForm())
