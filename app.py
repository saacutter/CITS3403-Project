from flask import Flask, render_template, request, redirect

# Initialise the Flask server
app = Flask(__name__)

# Default route of the application
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")