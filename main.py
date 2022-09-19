#!/usr/bin/env python
"""
To run type: flask --app hello run
"""

import datetime
import time

import numpy as np
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from config_files.config import config
from scripts.invoice import Invoice, get_new_invoice_number, get_number_of_invoices_in_db
from scripts.persons import Issuer, User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.update(config)
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route("/")
@app.route("/home")
def home():
    current_year = datetime.date.today().year
    return render_template(
        "index.html", current_year=current_year, logged_in=current_user.is_authenticated
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("user"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get("email")).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salted_password,
            surname=request.form.get("surname"),
            phone_no=request.form.get("phone_no"),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("user"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        # print(email)
        # Email doesn't exist or password incorrect.
        if not user:
            # print("not")
            flash("That email does not exist, please sign up for free.")
            time.sleep(3)
            return redirect(url_for("register"))
        else:
            # print("yes")
            login_user(user)
            return redirect(url_for("user"))

    return render_template("reset_password.html", logged_in=current_user.is_authenticated)


@app.route("/user")
@login_required
def user():
    return render_template("user.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/new-invoice", methods=["GET", "POST"])
@login_required
def new_invoice():
    print("NEW INVOICE")
    today = datetime.datetime.now()
    print("TODAY")
    if request.method == "POST":
        print("IF")
        new_invoice = Invoice(
            # invoice_type=request.args.get("invoice_type"),
            id=get_number_of_invoices_in_db(),
            invoice_type="regular",
            invoice_no=get_new_invoice_number(),
            issue_date=today.strftime("%d/%m/%Y"),
            issue_city=request.form.get("issue_city"),
            sell_date=today.strftime("%d/%m/%Y"),
            issuer_tax_no=request.form.get("issuer_tax_no"),
            recipient_tax_no=request.form.get("recipient_tax_no"),
            position=request.form.get("position"),
            amount=request.form.get("amount"),
            unit=request.form.get("unit"),
            price_net=request.form.get("price_net"),
            tax_rate=request.form.get("tax_rate"),
            sum_net=request.form.get("sum_net"),
            sum_gross=request.form.get("sum_gross"),
        )
        db.session.add(new_invoice)
        print("ADDED")
        db.session.commit()
        print("COMMITTED")
        return redirect(url_for("user"), logged_in=current_user.is_authenticated)
    return render_template(
        "new_invoice.html",
        invoice_no=get_new_invoice_number(),
        issue_date=today.strftime("%Y-%m-%d"),
        sell_date=today.strftime("%Y-%m-%d"),
        # According to the Polish tax law it is allowed to issue an invoice 60 days before
        # or 90 days after the sell date.
        min_date=(today - datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
        max_date=(today + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
        logged_in=current_user.is_authenticated,
    )


if __name__ == "__main__":
    app.run(debug=True)
