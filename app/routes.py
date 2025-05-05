from app import application, db, models, forms
from flask import render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from hashlib import md5
import os
from PIL import Image

# Update the last seen time of the user before each request
@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.now(timezone.utc)
        db.session.commit()

# Default route of the application
@application.route("/")
def index():
    return render_template("index.html")

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    # Ensure that the user cannot access this route if they are already signed in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Extract the next page from the URL and add it to the form
    if request.method == "GET":
        next_page = request.args.get('next', 'index')

    form = forms.LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # Retrieve the user from the database based on the provided username/email address
        username = form.username.data
        user = db.session.scalar(sa.select(models.Users).where((models.Users.username == username) | (models.Users.email == username)))

        # Ensure that the user exists and that the password hash matches
        if user is None or not check_password_hash(user.password, form.password.data):
            flash("The username and password do not match")
            return redirect(url_for('login'))

        # Log the user in
        login_user(user, remember=form.remember_user.data)

        # Extract the next page from the form and redirect them to that page
        next_page = request.form.get('next')
        return redirect(url_for(next_page))
    return render_template("login.html", login=True, loginForm=form, signupForm=forms.RegistrationForm(), next=next_page) # Display login page

# Signup route of the application
@application.route("/register", methods=["GET", "POST"])
def signup():
    # Ensure that the user cannot access this route if they are already signed in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = forms.RegistrationForm()
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
        hashed_password = generate_password_hash(password)

        # Create the user entry and add it to the database
        user = models.Users(
            username=username, 
            password=hashed_password, 
            email=email,
            private=form.privacy.data,
            profile_picture='https://www.gravatar.com/avatar/' + md5(email.encode()).hexdigest() + '?d=identicon'
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

@application.route('/user/<username>')
def profile(username):
    # Get the user with the specified ID
    user = db.first_or_404(sa.select(models.Users).where(models.Users.username == username))
    return render_template("user.html", user=user)

@application.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = forms.EditProfileForm(private=current_user.private)

    if request.method == "POST" and form.validate_on_submit():
        # Extract the information from the form
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data.strip()
        image = request.files['profile_picture'] # Adapted from https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

        # Check that the password is valid
        if password and len(password) < 8:
            flash("The password must be at least 8 characters long")
            return redirect(url_for('edit_profile'))
        
        # Check if username or email already exists
        existing_user = db.session.scalar(sa.select(models.Users).where((models.Users.username == username) | (models.Users.email == email)))
        if existing_user and existing_user != current_user:
            flash("A user with this username or email address already exists!")
            return redirect(url_for('edit_profile'))
        
        # Save the uploaded image to the server if one was uploaded
        img_filename = secure_filename(image.filename)
        if img_filename != "": 
            img = Image.open(image)  
            max_width, max_height = 500, 500 
            if img.width > max_width or img.height > max_height:  
                flash(f"The image resolution is too large. Max allowed is {max_width}x{max_height}px.")  
                return redirect(url_for('edit_profile')) 

            # Ensure that the extension is a valid image extension
            extension = os.path.splitext(img_filename)[1]
            if extension not in application.config['UPLOAD_EXTENSIONS']:
                flash("The profile image can only be in .png, .jpeg or .webp format")
                return redirect(url_for('edit_profile'))

            # Save the image to a known location on the server (no extension to not fill up the server)
            image.save(os.path.join(application.config['UPLOAD_PATH'], str(current_user.id)))
        
        # Update the user information based on the provided information
        user = models.Users.query.get(current_user.id)
        user.username = username
        user.email = email
        user.private = form.private.data
        if password: user.password = generate_password_hash(password)
        if image: user.profile_picture = str(current_user.id)
        
        # Save the new information to the database
        db.session.commit()

        return redirect(url_for('profile', username=current_user.username))
    return render_template("edit-profile.html", form=form)

@application.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(application.config['UPLOAD_PATH'], filename)

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
        ...
    
    # Return an empty JSON object if no users match the specified pattern
    if len(users) == 0:
      return jsonify([{"username": None}])

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