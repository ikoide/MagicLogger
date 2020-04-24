import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Markup, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from mtglogger import app, db, bcrypt
from mtglogger.forms import SearchForm
from mtglogger.scripts.card import find_card
from mtgsdk import Card

@app.route("/", methods=['GET', 'POST'])
def home():
  form = SearchForm()

  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
    form.query.data = None
  return render_template("index.html", form=form, title="Home")

@app.route("/results/<search_query>", methods=['GET', 'POST'])
def results(search_query):
  x = find_card(search_query)

  form = SearchForm()
  if form.validate_on_submit():
    return redirect(url_for('results', search_query=form.query.data))
    form.query.data = None

  return render_template("results.html", cards=x[0], total_cards=x[1], form=form, title="Query")

# Auth

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = SearchForm()

  return render_template("auth/login.html", title="Login", form=form)