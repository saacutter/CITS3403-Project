from app import application, db, models, forms
from flask import render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from flask import abort
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timezone, date
from hashlib import md5
import os
from PIL import Image

# Update the last seen time of the user before each request
@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.now(timezone.utc)
        db.session.commit()

@application.errorhandler(404)
def page_not_found(error_code):
    return render_template("404.html"), 404

# Default route of the application
@application.route("/")
def index():
    # Get the 8 most recent public tournaments
    public = models.Tournaments.query.join(models.Users, models.Tournaments.user_id == models.Users.id).filter(models.Users.private == False).order_by(models.Tournaments.date.desc()).limit(8).all()

    # Get the 8 most recent tournaments from followed users
    friends = models.Tournaments.query.join(models.Friends, models.Tournaments.user_id == models.Friends.from_user).filter(models.Friends.to_user == current_user.id).order_by(models.Tournaments.date.desc()).limit(8).all() if current_user.is_authenticated else []
    
    return render_template("home.html", public_tournaments=public, friend_tournaments=friends)

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
        username = form.username.data.lower()
        user = db.session.scalar(sa.select(models.Users).where((sa.func.lower(models.Users.username) == username) | (models.Users.email == username)))

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

@application.route('/tournaments')
def browse():
    # Retrieve all of the tournaments in the database and order by descending date order (newest first)
    tournaments = models.Tournaments.query.join(models.Users, models.Tournaments.user_id == models.Users.id).filter(models.Users.private == False).order_by(models.Tournaments.date.desc()).all()
    return render_template("tournaments.html", tournaments=tournaments)

@application.route('/user/<username>')
def profile(username):
    # Get the user with the specified ID
    user = db.first_or_404(sa.select(models.Users).where(models.Users.username == username))

    # Get the users that the current user is following
    users_followed = list(db.session.scalars(sa.select(models.Users).join(models.Friends, models.Users.id == models.Friends.to_user).where(models.Friends.from_user == user.id)))

    # Get the user's following the current user
    users_following = list(db.session.scalars(sa.select(models.Users).join(models.Friends, models.Users.id == models.Friends.from_user).where(models.Friends.to_user == user.id)))

    # Get the user's tournament data and calculate statistics
    tournaments =  models.Tournaments.query.filter_by(user_id=user.id).all()
    total_games = len(tournaments)
    wins = sum(1 for m in tournaments if m.result.lower() == 'win')
    losses = sum(1 for m in tournaments if m.result.lower() == 'loss')
    draws = sum(1 for m in tournaments if m.result.lower() == 'draw')
    win_pct = round((wins / total_games) * 100, 2) if total_games > 0 else 0.00
    avg_points = round(sum(m.points for m in tournaments) / total_games, 2) if total_games > 0 else 0.00
    statistics = {'total_games': total_games, 'wins': wins, 'losses': losses, 'draws': draws, 'win_pct': win_pct, "avg_points": avg_points}

    return render_template("user.html", user=user, following=users_followed, followers=users_following, statistics=statistics)

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
            flash("A user with this username or email address already exists")
            return redirect(url_for('edit_profile'))
        
        # Save the uploaded image to the server if one was uploaded
        img_filename = secure_filename(image.filename)
        if img_filename != "":
            # Ensure that the image is roughly square (with a 50px tolerance)
            img = Image.open(image)   
            if abs(img.width - img.height) > 50:
                flash("The profile image must be square")
                return redirect(url_for('edit_profile'))
            image.seek(0) # Reset the file point to the start so that it can be saved to the server properly
            
            # Ensure that the extension is a valid image extension
            extension = os.path.splitext(img_filename)[1]
            if extension not in application.config['UPLOAD_EXTENSIONS']:
                flash("The profile image can only be in .png, .jpeg or .webp format")
                return redirect(url_for('edit_profile'))

            # Save the image to a known location on the server (no extension to not fill up the server)
            image.save(os.path.join(application.config['PFP_UPLOAD_PATH'], str(current_user.id)))
        
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
    if os.path.exists(os.path.join(application.config['PFP_UPLOAD_PATH'], filename)): # Check for profile images
        return send_from_directory(application.config['PFP_UPLOAD_PATH'], filename)
    elif os.path.exists(os.path.join(application.config['TP_UPLOAD_PATH'], filename)): # Check for tournament images
        return send_from_directory(application.config['TP_UPLOAD_PATH'], filename)
    else:
        return send_from_directory(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/img/'), 'default.png') # Send a file not found image if nothing is found
        # Retrieved from https://en.m.wikipedia.org/wiki/File:No_photo_available.svg

@application.route('/search')
@login_required
def search():
    return render_template("search.html")

@application.route('/get_like/<pattern>')
def get_like(pattern):
    # Extract the users from the database that begin with the requested pattern
    users = db.session.scalars(sa.select(models.Users).where(models.Users.username.like(pattern + '%'))).all()

    # Get the friends of the current user
    friends = db.session.scalars(sa.select(models.Friends.to_user).where(models.Friends.from_user == current_user.id)).all()

    # Create a list of results that gets all users that match the pattern and aren't already friends with the current user
    results = [user.serialise() for user in users if user.id != current_user.id and user.id not in friends]

    # TODO: Create an attribute if the user is friends with a user and show that on the results by removing the button
    
    # Return an empty JSON object if no users match the specified pattern
    if len(results) == 0:
      results = [{"username": None}]

    # Return a JSON object of the extracted users
    return jsonify(results) # Adapted from: https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask

@application.route('/add_friend/<username>', methods=["POST"])
def add_friend(username):
    # Retrieve the user with the given username
    user = db.session.scalar(sa.select(models.Users).where(models.Users.username == username))

    # Return an error message if the user is the current user
    if user.id == current_user.id:
        return '', 400
    
    # Ensure that the user has not already added the user
    relationship = db.session.scalar(sa.select(models.Friends).where((models.Friends.from_user == current_user.id) & (models.Friends.to_user == user.id)))
    if relationship:
        return '', 400

    # Create an object that adds the user with the current user
    friend = models.Friends(
        to_user=user.id,
        from_user=current_user.id
    )

    # Add this relationship to the database
    db.session.add(friend)
    db.session.commit()

    return '', 200

@application.route('/remove_friend/<username>', methods=["POST"])
def remove_friend(username):
    # Retrieve the user with the given username
    user = db.session.scalar(sa.select(models.Users).where(models.Users.username == username))

    # Return an error message if the user is the current user
    if user.id == current_user.id:
        return '', 400
    
    # Ensure that the user is friends with the requested user
    relationship = db.session.scalar(sa.select(models.Friends).where((models.Friends.from_user == current_user.id) & (models.Friends.to_user == user.id)))
    if not relationship:
        return '', 400

    # Remove the relationship from the database
    db.session.delete(relationship)
    db.session.commit()

    return '', 200

@application.route('/addTournament', methods=["GET", "POST"])
@login_required
def tournament():
    form = forms.AddTournamentForm()

    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        date = form.date.data.strftime('%Y-%m-%d')
        points = form.points.data
        result = form.result.data.lower().strip()
        image = request.files['preview']

        # Ensure that the date is earlier than the current day
        if date > str(datetime.now().strftime("%Y-%m-%d")):
            flash("The tournament cannot be after today's date (" + str(datetime.now().strftime("%Y-%m-%d")) + ")")
            return redirect(url_for('tournament'))
        
        # Ensure that the points is a numeric value
        try:
            points = int(points)
        except ValueError:
            flash("The points must be a numeric value")
            return redirect(url_for('tournament'))

        # Check that the result is valid
        if result not in ["win", "loss", "draw"]:
            flash("The result can only be a 'win', 'loss', or 'draw'")
            return redirect(url_for('tournament'))

        # Save the uploaded image to the server if one was uploaded
        img_filename = secure_filename(image.filename)
        if img_filename != "":
            # Ensure that the image is roughly square (with a 50px tolerance)
            img = Image.open(image)   
            if abs(img.width - img.height) > 50:
                flash("The profile image must be square")
                return redirect(url_for('tournament'))
            image.seek(0) # Reset the file point to the start so that it can be saved to the server properly
            
            # Ensure that the extension is a valid image extension
            extension = os.path.splitext(img_filename)[1]
            if extension not in application.config['UPLOAD_EXTENSIONS']:
                flash("The profile image can only be in .png, .jpeg or .webp format")
                return redirect(url_for('tournament'))

            # Save the image to a known location on the server (no extension to not fill up the server)
            img_filename = name + '-' + date + '-' + str(current_user.id)
            image.save(os.path.join(application.config['TP_UPLOAD_PATH'], img_filename))

        # Create and save tournament
        tournament = models.Tournaments(
            user_id=current_user.id,
            name=name,
            game_title=form.game.data.strip(),
            date=date,
            points=points,
            result=result,
            details=form.details.data,
            image=img_filename or "https://static.vecteezy.com/system/resources/thumbnails/017/287/469/small_2x/joystick-for-game-console-computer-ps-line-icon-joypad-game-controller-for-videogame-pictogram-computer-gamepad-play-equipment-outline-symbol-editable-stroke-isolated-illustration-vector.jpg" # Retrieved from https://www.vecteezy.com/vector-art/17287469-joystick-for-game-console-computer-ps-line-icon-joypad-game-controller-for-videogame-pictogram-computer-gamepad-play-equipment-outline-symbol-editable-stroke-isolated-vector-illustration
        )
        db.session.add(tournament)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("add-tournament.html", form=form)

@application.route('/delete_tournament/<id>', methods=["POST"])
def remove_tournament(id):
    # Retrieve the tournament with the given ID and ensure it belongs to the current user
    tournament = db.session.scalar(sa.select(models.Tournaments).where((models.Tournaments.id == id) & (models.Tournaments.user_id == current_user.id)))
    if not tournament:
        return '', 400

    # Remove the tournament from the database
    db.session.delete(tournament)
    db.session.commit()

    return '', 200

@application.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy-policy.html')
