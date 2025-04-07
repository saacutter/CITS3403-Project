from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialise the Flask server
app = Flask(__name__)

# Create the database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Default route of the application
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)