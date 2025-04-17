from app import application, db, migrate, models
from flask import render_template, request, redirect, url_for, session

# Default route of the application
@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")