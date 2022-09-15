#!/usr/bin/env python
"""
To run type: flask --app hello run
"""

import datetime
import sqlite3
import time

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

from scripts.invoice import Invoice, get_new_invoice_number
from scripts.persons import User

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret-key-goes-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


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


@app.route("/new-invoice")
@login_required
def new_invoice():
    today = datetime.datetime.now()
    if request.method == "POST":
        invoice_type = request.form["invoice_type"]
        issuer_tax_no = request.form["issuer_tax_no"]
        recipient_tax_no = request.form["recipient_tax_no"]
        position = request.form["position"]
        amount = request.form["amount"]
        price_net = request.form["price_net"]
        tax_rate = request.form["tax_rate"]
        new_invoice = Invoice(
            invoice_type=invoice_type,
            issuer_tax_no=issuer_tax_no,
            recipient_tax_no=recipient_tax_no,
            position=position,
            amount=amount,
            price_net=price_net,
            tax_rate=tax_rate,
        )
        db.session.add(new_invoice)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template(
        "new_invoice.html",
        invoice_number=get_new_invoice_number(),
        issue_date=today.strftime("%Y-%m-%d"),
        net_sum=Invoice.price_net * Invoice.amount,
        # gross_sum=Invoice.price_net * Invoice.tax_rate + Invoice.price_net,
        gross_sum=None,
        # According to the Polish tax law it is allowed to issue an invoice 60 days before
        # or 90 days after the sell date.
        min_date=(today - datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
        max_date=(today + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
    )


if __name__ == "__main__":
    app.run(debug=True)
