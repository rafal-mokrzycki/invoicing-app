#!/usr/bin/env python
"""
To run type: flask --app hello run
"""

import datetime
import sqlite3

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
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
def load_user(user_id):
    return User.query.get(int(user_id))


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
            return redirect(url_for("secrets"))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        surname = request.form["surname"]
        phone_no = request.form["phone_no"]
        password = request.form["password"]
        new_user = User(
            email=email,
            name=name,
            surname=surname,
            phone_no=phone_no,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")


@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/new-invoice")
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


def create_table(name="accounts"):
    cursor = sqlite3.connect("database.db", check_same_thread=False).cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {name} (
            email varchar(250) PRIMARY KEY,
            surname varchar(250) NOT NULL,
            name varchar(250) NOT NULL,
            phone_no varchar(250) NOT NULL,
            password varchar(250) NOT NULL)"""
    )


if __name__ == "__main__":
    app.run(debug=True)
