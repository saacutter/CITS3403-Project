from app import application, db, migrate, models, forms
from flask import render_template, request, redirect, url_for, session

# Default route of the application
@application.route("/")
@application.route("/index")
def index():
    user = {'username': 'username', 'image': 'https://picsum.photos/200'} 
    return render_template("index.html", signed_out=True, user=user)

# Login route of the application
@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and forms.LoginForm().validate_on_submit():
        ... # TODO: Create the sign in logic
        return redirect(url_for('index'))
    return render_template("login.html", signed_out=True, login=True, loginForm=forms.LoginForm(), signupForm=forms.SignupForm())

# Signup route of the application
@application.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = forms.SignupForm()
    if request.method == "POST" and signup_form.validate_on_submit():
        new_user = models.Users(
            username=signup_form.username.data,
            email=signup_form.email.data,
            password=signup_form.password.data,
            privacy=signup_form.privacy.data
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    
    return render_template("login.html", signed_out=True, login=False, loginForm=forms.LoginForm(), signupForm=signup_form)
