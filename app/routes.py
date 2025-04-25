from app import application, db, migrate, models
from flask import render_template, request, redirect, url_for, session

# Default route of the application
@application.route("/")
def index():
    return render_template("index.html", signed_out=True)

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ... # TODO: Create the sign in logic
        return redirect("/")
    return render_template("login.html", signed_out=True, login=True) # Display login page
        
# Signup route of the application
@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        ... # TODO: Create the sign up logic
        return redirect("/")
    return render_template("login.html", signed_out=True, login=False) # Display sign up page