from app import application
from flask import render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Default route of the application
@application.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")