from app import application, db, models, forms
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import re

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
    
    form = forms.LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # Retrieve the user from the database based on the provided username/email address
        username = form.username.data
        user = db.session.scalar(sa.select(models.Users).where((models.Users.username == username) | (models.Users.email == username)))

        # Ensure that the user exists and that the password hash matches
        if user is None or not check_password_hash(user.password, form.password.data):
            flash("The username and password do not match")
            return redirect(url_for('login'))
        
        # Update the user's last login time and commit it to the database
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # Log the user in
        login_user(user, remember=form.remember_user.data)

        # Extract the next page from the URL and redirect them to that page
        next_page = request.args.get('next', 'index')
        return redirect(url_for(next_page))
    return render_template("login.html", login=True, loginForm=form, signupForm=forms.SignupForm()) # Display login page

# Signup route of the application
@application.route("/register", methods=["GET", "POST"])
def signup():
    # Ensure that the user cannot access this route if they are already signed in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = forms.SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        # Extract the information from the form
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data.strip()

        # Check that the password is valid
        if len(password) < 8:
            flash("The password must be at least 8 characters long")
            return redirect(url_for('signup'))
        
        # Ensure that the passwords on the form match
        if password != form.password_confirm.data:
            flash("The passwords do not match")
            return redirect(url_for('signup'))
        
        # Check if username or email already exists
        existing_user = db.session.scalar(sa.select(models.Users).where((models.Users.username == username) | (models.Users.email == email)))
        if existing_user:
            flash("A user with this username or email address already exists!")
            return redirect(url_for('signup')) 
        
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Create the user entry and add it to the database
        user = models.Users(
            username=username, 
            password=hashed_password, 
            email=email,
            privacy=form.privacy.data
        )
        db.session.add(user)
        db.session.commit()

        # Log in the user and redirect them to the homepage
        login_user(user, remember=True)
        return redirect('/')
    return render_template("login.html", login=False, loginForm=forms.LoginForm(), signupForm=form) # Display sign up page

@application.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/search')
@login_required
def search():
    return render_template("search.html")

@application.route('/get_like/<pattern>')
def get_like(pattern):
    # Extract the users from the database that begin with the requested pattern
    users = db.session.scalars(sa.select(models.Users).where(models.Users.username.like(pattern + '%'))).all()

    # Remove the signed in user from the list, if applicable
    try:
        users.remove(current_user)
    except ValueError:
        return jsonify([{"username": None}]) 
    
    # Return an empty JSON object if no users match the specified pattern
    if len(users) == 0:
      return jsonify({"username": None})

    # Return a JSON object of the extracted users
    return jsonify([user.serialise() for user in users]) # Adapted from: https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask

@application.route('/addMatch', methods=["GET", "POST"])
@login_required
def match():
    if request.method == "POST" and forms.AddMatchForm().validate_on_submit():
        form = forms.AddMatchForm()

        # Extract the information from the request
        file = request.files['file']
        game = form.game.data
        points = form.points.data
        time_taken = form.time_taken.data
        result = form.result.data

        # Ensure that valid data was provided
        if file == None or (game == "" and points == "" and time_taken == "" and result == ""):
            return redirect(url_for('match'))

        if file:
            # TODO: Process the file (requires the format of file to be specified)
            ...
        else:
            # Create the match entry and add it to the database
            data_entry = models.Matches(user_id=current_user.id, game=game, points=points, time_taken=time_taken, result=result)
            db.session.add(data_entry)
            db.session.commit()

        return redirect(url_for('index'))
    return render_template("add-match.html", form=forms.AddMatchForm())

@application.route('/addTournament', methods=["GET", "POST"])
@login_required
def tournament():
    if request.method == "POST" and forms.AddTournamentForm().validate_on_submit():
        form = forms.AddTournamentForm()

        # Extract the information from the request
        file = request.files['file']
        name = form.name.data
        game = form.game.data
        time = form.time.data

        # Ensure that valid data was provided
        if file == None or (name == "" and game == "" and time == ""):
            return redirect(url_for('tournament'))

        if file:
            # TODO: Process the file (requires the format of file to be specified)
            ...
        else:
            # Create the tournament entry and add it to the database
            data_entry = models.Tournaments(name=name, game=game, time=time)
            db.session.add(data_entry)
            db.session.commit()

        return redirect(url_for('index'))
    return render_template("add-tournament.html", form=forms.AddTournamentForm())