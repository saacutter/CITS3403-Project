from app import application, db, migrate, models, forms
from flask import render_template, request, redirect, url_for, session

# Default route of the application
@application.route("/")
@application.route("/index")
def index():
    user = {'username': 'username', 'image': 'https://picsum.photos/200'} # This is just a temporary user where the image is a random image
    return render_template("index.html", signed_out=True, user=user) # TODO: signed_out can be assigned to the .is_authenticated method when we come to that

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and forms.LoginForm().validate_on_submit():
        ... # TODO: Create the sign in logic
        return redirect(url_for('index'))
    return render_template("login.html", signed_out=True, login=True, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display login page
        
# Signup route of the application
@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST" and forms.SignupForm().validate_on_submit():
        ... # TODO: Create the sign up logic
        return redirect(url_for('index'))
    return render_template("login.html", signed_out=True, login=False, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display sign up page