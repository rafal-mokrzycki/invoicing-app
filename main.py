#!/usr/bin/env python
"""
To run type: flask --app hello run
"""

import datetime
import time

import numpy as np
import pdfkit
import sqlalchemy
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
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
from scripts.database import Contractor, Database, User
from scripts.invoice import (
    Invoice,
    format_number,
    format_percentages,
    get_number_of_invoices_in_db,
)

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


@app.route("/new_invoice", methods=["GET", "POST"])
@login_required
def new_invoice():
    today = datetime.datetime.now()
    if request.method == "POST":
        new_invoice = Invoice(
            id=get_number_of_invoices_in_db(),
            invoice_type=request.form.get("invoice_type"),
            invoice_no=request.form.get("invoice_no"),
            issue_date=today.date(),
            issue_city=request.form.get("issue_city"),
            sell_date=datetime.datetime.strptime(
                request.form.get("sell_date"), "%Y-%m-%d"
            ).date(),
            issuer_tax_no=request.form.get("issuer_tax_no"),
            recipient_tax_no=request.form.get("recipient_tax_no"),
            item=request.form.get("posiitem
            amount=request.form.get("amount"),
            unit=request.form.get("unit"),
            price_net=request.form.get("price_net"),
            tax_rate=request.form.get("tax_rate"),
            sum_net=request.form.get("sum_net"),
            sum_gross=request.form.get("sum_gross"),
        )
        db.session.add(new_invoice)
        db.session.commit()
        return redirect(url_for("user"))
    return render_template(
        "new_invoice.html",
        # According to the Polish tax law it is allowed to issue an invoice 60 days before
        # or 90 days after the sell date.
        today=today.date(),
        min_date=(today - datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
        max_date=(today + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
        logged_in=current_user.is_authenticated,
    )


@app.route("/your_invoices", methods=["GET", "POST"])
@login_required
def your_invoices():
    if request.method == "POST":
        pass
    else:
        invoices = Invoice.query.order_by(Invoice.issue_date).all()
        return render_template("your_invoices.html", invoices=invoices)
    return render_template("your_invoices.html")


@app.route("/your_invoices/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    invoice = Invoice.query.get_or_404(id)
    if request.method == "POST":
        invoice.id = invoice.id
        invoice.invoice_type = request.form.get("invoice_type")
        invoice.invoice_no = request.form.get("invoice_no")
        invoice.issue_date = request.form.get("issue_date")
        invoice.issue_city = request.form.get("issue_city")
        invoice.sell_date = datetime.datetime.strptime(
            request.form.get("sell_date"), "%Y-%m-%d"
        ).date()
        invoice.issuer_tax_no = request.form.get("issuer_tax_no")
        invoice.recipient_tax_no = request.form.get("recipient_tax_no")
        invoice.item = request.form.get("posiitem
        invoice.amount = request.form.get("amount")
        invoice.unit = request.form.get("unit")
        invoice.price_net = request.form.get("price_net")
        invoice.tax_rate = request.form.get("tax_rate")
        invoice.sum_net = request.form.get("sum_net")
        invoice.sum_gross = request.form.get("sum_gross")
        try:
            db.session.commit()
            return render_template("your_invoices.html")
        except:
            return "HELLO"
    return render_template("edit_invoice.html", invoice=invoice)


@app.route("/your_invoices/show/<int:id>", methods=["GET", "POST"])
@login_required
def show_pdf(id):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    invoice = Invoice.query.get_or_404(id)
    rendered = render_template(
        "pdf_template.html",
        amount=invoice.amount,
        invoice_no=invoice.invoice_no,
        invoice_type=invoice.invoice_type.upper(),
        issue_city=invoice.issue_city,
        issue_date=invoice.issue_date,
        issuer_tax_no=invoice.issuer_tax_no,
        item=invoice.posiitem
        price_net=format_number(invoice.price_net),
        recipient_tax_no=invoice.recipient_tax_no,
        sell_date=invoice.sell_date,
        sum_gross=format_number(invoice.sum_gross),
        sum_net=format_number(invoice.sum_net),
        tax_string=format_percentages(invoice.tax_rate),
        unit=invoice.unit,
    )
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers[
        "Content-Disposition"
    ] = f"inline; filename=Invoice_no_{invoice.invoice_no}.pdf"
    return response


if __name__ == "__main__":
    app.run(debug=True)
