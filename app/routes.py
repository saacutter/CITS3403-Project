from app import application, db, migrate, models, forms
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

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
            # TODO: Display error message for incorrect password/username
            return redirect(url_for('login'))
        
        # Update the user's last login time and commit it to the database
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # Log the user in
        login_user(user, remember=form.remember_user.data)

        # Extract the next page from the URL and redirect them to that page
        next_page = request.args.get('next', 'index')
        return redirect(url_for(next_page))
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
            # TODO: Display error message because the passwords do not match
            return redirect(url_for('login'))
          
        email = form.email.data.strip().lower()
        username = form.username.data.strip()
        
        # Check if username or email already exists
        existing_user = db.session.scalar(sa.select(models.Users).where((models.Users.username == username) | (models.Users.email == email)))
        if existing_user: return redirect(url_for('signup')) 
        
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)
        
        # TODO: Validate the username and email addresses (both by confirming that they are not already in the database and ensuring they are valid)
        # Usernames should only consists of letters and numbers (this can be validated with a regex like r"$[a-zA-Z0-9]+^")
        # Emails can be validated by using a regex taken from the internet

        # Create the user entry and add it to the database
        user = models.Users(
          username=username, 
          password=hashed_password, 
          email=email,
          privacy=form.privacy.data)
        db.session.add(user)
        db.session.commit()

        # Log in the user and redirect them to the homepage
        login_user(user, remember=True)
        return redirect('/')
    return render_template("login.html", login=False, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display sign up page

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
