import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory
from mtglogger import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from mtglogger.forms import SearchForm, LoginForm, RegistrationForm, AddForm
from mtglogger.models import User, Card
from mtglogger.scripts.card import by_name, by_multiverseId, return_card

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title="404 Error"), 404

@app.route("/", methods=['GET', 'POST'])
def home():
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
  
  return render_template("index.html", form=form, title="Home")

@app.route("/search/<search_query>", methods=['GET', 'POST'])
def results(search_query):
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
  
  cards = by_name(search_query)
  
  return render_template("results.html", form=form, title="Search", cards=cards)

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

  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))

  return render_template("auth/login.html", form=form, title="Login", loginForm=loginForm)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))

  return render_template("auth/register.html", form=form, title="Register", registrationForm=registrationForm)

@app.route("/collection", methods=['GET', 'POST'])
@login_required
def collection():
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
  
  act_cards = []
  for i in current_user.cards:
    card = return_card(i.multiverse_id)
    card["quantity"] = i.quantity
    act_cards.append(card)
  return render_template("collection.html", form=form, title="Collection", act_cards=act_cards)

@app.route("/card/<multiverse_id>", methods=['POST', 'GET'])
def card(multiverse_id):
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
  
  card = return_card(multiverse_id)
  if card:
    page_title = card["name"]
  else:
    page_title = "Not Valid Card"

  addForm = AddForm()
  if addForm.validate_on_submit():
    if not current_user.is_authenticated:
      flash('You must login to add cards to your collection.', 'warning')
      return redirect(url_for('login'))
    else:
      card = Card(multiverse_id=multiverse_id, quantity=int(addForm.quantity.data), owner=current_user)
      db.session.add(card)
      db.session.commit()
      return redirect(url_for('collection'))

  return render_template("card.html", form=form, title=page_title, addForm=addForm, card=card)

@app.route("/trades", methods=['GET', 'POST'])
@login_required
def trades():
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
  
  return render_template("trades.html", form=form, title="Trades")