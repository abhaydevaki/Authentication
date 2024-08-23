from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# we import user to store the user's data
# we import the securities and hashs to basically encrypt our password
# it is a special encryption where you can't get the orginal value by decrypting
# insted you have to run the same original password into the encryption and check is the result is same or not
# current user hold the current information of the user i.e if he/she has logged in or is at home page or is logged out
# we can use this current user module as we used UserMixin in the models file

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            
            else:
                flash("Incorrect password, try again.",category="error")
        else:
            flash("Email does not exist.", category="error")
        
    return render_template("login.html", user=current_user)
    # return render_template("login.html", boolean=True, text="Testing", user="Abhay", work="website")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        elif password1 != password2:
            flash("Passwords must be same.", category="error")
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters.", category="error")
        else:
            # add user to database
            # scrypt is a hashing algorithm
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    
    return render_template("sign_up.html", user=current_user)


