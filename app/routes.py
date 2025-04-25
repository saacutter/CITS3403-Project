from app import application, db, migrate, models, forms
from flask import render_template, request, redirect, url_for, session

# Default route of the application
@application.route("/")
def index():
    return render_template("index.html", signed_out=True)

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and forms.LoginForm().validate_on_submit():
        ... # TODO: Create the sign in logic
        return redirect("/")
    return render_template("login.html", signed_out=True, login=True, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display login page
        
# Signup route of the application
@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST" and forms.SignupForm().validate_on_submit():
        ... # TODO: Create the sign up logic
        return redirect("/")
    return render_template("login.html", signed_out=True, login=False, loginForm=forms.LoginForm(), signupForm=forms.SignupForm()) # Display sign up page