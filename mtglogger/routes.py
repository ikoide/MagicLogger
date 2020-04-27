import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory
from mtglogger import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mtglogger.forms import SearchForm, LoginForm, RegistrationForm
from mtglogger.models import User
from mtglogger.scripts.card import get_card

@app.route("/", methods=['GET', 'POST'])
def home():
  
  return render_template("index.html", title="Home")

@app.route("/search/<search_query>", methods=['GET', 'POST'])
def results(search_query):
  cards = get_card(search_query)
  
  return render_template("results.html", title="Search", cards=cards)

# Auth

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    flash('Your already logged in.', 'info')
    return redirect(url_for('home'))

  loginForm = LoginForm()

  if loginForm.validate_on_submit() and loginForm.submit.data:
    user = User.query.filter_by(username=loginForm.username.data).first()
    if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
      login_user(user)
      next_page = request.args.get('next')
      message = Markup('Login successful! Welcome back <b>' + current_user.username + '</b>.')
      flash(message, 'success')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login unsuccessful, please check your username and password.', 'danger')


  return render_template("auth/login.html", title="Login", loginForm=loginForm)

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    flash('Your already logged in.', 'info')
    return redirect(url_for('home'))

  registrationForm = RegistrationForm()

  if registrationForm.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
    user = User(username=registrationForm.username.data, email=registrationForm.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You are now able to login.', 'success')
    return redirect(url_for('login'))

  return render_template("auth/register.html", title="Register", registrationForm=registrationForm)

@app.route("/collection", methods=['GET', 'POST'])
def collection():
  return render_template("collection.html", title="Collection")