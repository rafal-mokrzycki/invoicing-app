#!/usr/bin/env python
"""
Main module. To run type:
'path/to/python.exe' app.py
"""
import datetime
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import repackage

repackage.up(1)
import calendar

import pdfkit
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Date, Float, Integer, String, create_engine, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from config_files.config import credentials, settings
from scripts.formatters import (
    format_number,
    format_percentages,
    get_number_of_objects_in_table,
)
from scripts.helpers import append_dict, get_currencies
from scripts.models import *

CURRENCY = "PLN"

# app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)
# app.config.update(credentials)
# mail = Mail(app)
# db = SQLAlchemy(app)
# Base = declarative_base()
# engine = create_engine(credentials["SQLALCHEMY_DATABASE_URI"])
# db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


# def clear_the_template_cache():
#     app.jinja_env.cache = {}


# app.before_request(clear_the_template_cache)
app = Flask(__name__)
app.config.update(credentials)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        body = request.form.get("body")
        msg = Message(
            subject=f'New email from {name}. "{subject}"',
            body=body,
            sender=email,
        )
        mail.send(msg)
        # return f"{msg}"
        return render_template(
            "index.html",
            msg_sent=True,
            current_year=datetime.date.today().year,
            logged_in=current_user.is_authenticated,
        )
    return render_template(
        "index.html",
        msg_sent=False,
        current_year=datetime.date.today().year,
        logged_in=current_user.is_authenticated,
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
            plan=request.form.get("plan"),
            # terms=request.form.get("terms") or False,
            # newsletter=request.form.get("newsletter") or False,
            terms=bool(request.form.get("terms")),
            newsletter=bool(request.form.get("newsletter")),
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
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
        new_invoice = InvoiceForm(
            id=get_number_of_objects_in_table(Invoice),
            invoice_type=request.form.get("invoice_type"),
            invoice_no=request.form.get("invoice_no"),
            issue_date=today.date(),
            issue_city=request.form.get("issue_city"),
            sell_date=datetime.datetime.strptime(
                request.form.get("sell_date"), "%Y-%m-%d"
            ).date(),
            issuer_tax_no=request.form.get("issuer_tax_no"),
            recipient_tax_no=request.form.get("recipient_tax_no"),
            item=request.form.get("item"),
            amount=request.form.get("amount"),
            unit=request.form.get("unit"),
            price_net=request.form.get("price_net"),
            tax_rate=request.form.get("tax_rate"),
            sum_net=request.form.get("sum_net"),
            sum_gross=request.form.get("sum_gross"),
            currency=request.form.get("currency"),
        )
        db_session.add(new_invoice)
        db_session.commit()
        return redirect(url_for("user"))
    return render_template(
        "new_invoice.html",
        # According to the Polish tax law it is allowed to issue an invoice 60 days before
        # or 90 days after the sell date.
        today=today.date(),
        min_date=(today - datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
        max_date=(today + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
        logged_in=current_user.is_authenticated,
        year_month=datetime.datetime.strftime(today, "%Y/%m/"),
        invoice_number_on_type=get_dict_with_invoices_counted(InvoiceForm),
        currencies=get_currencies(),
    )


@app.route("/your_invoices", methods=["GET", "POST"])
@login_required
def your_invoices():
    if request.method == "POST":
        pass
    else:
        invoices = InvoiceForm.query.order_by(InvoiceForm.issue_date).all()
        return render_template("your_invoices.html", invoices=invoices)
    return render_template("your_invoices.html")


@app.route("/your_invoices/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Method enables edition of existing invoices"""
    invoice = Invoice.query.get_or_404(id)
    print(type(invoice))
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
        invoice.item = request.form.get("item")
        invoice.amount = request.form.get("amount")
        invoice.unit = request.form.get("unit")
        invoice.price_net = request.form.get("price_net")
        invoice.tax_rate = request.form.get("tax_rate")
        invoice.sum_net = request.form.get("sum_net")
        invoice.sum_gross = request.form.get("sum_gross")
        try:
            db_session.commit()
            return redirect(url_for("your_invoices"))
        except SQLAlchemyError:
            print("There was an error.")
    return render_template("edit_invoice.html", invoice=invoice)


@app.route("/your_invoices/show/<int:id>", methods=["GET", "POST"])
@login_required
def show_pdf(id, download=False):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    invoice = InvoiceForm.query.get_or_404(id)
    rendered = render_template(
        "pdf_template.html",
        amount=invoice.amount,
        invoice_no=invoice.invoice_no,
        invoice_type=invoice.invoice_type.upper(),
        issue_city=invoice.issue_city,
        issue_date=invoice.issue_date,
        issuer_tax_no=invoice.issuer_tax_no,
        item=invoice.item,
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
    if download:
        response.headers[
            "Content-Disposition"
        ] = f"attachment; filename=Invoice_no_{invoice.invoice_no}.pdf"
    else:
        response.headers[
            "Content-Disposition"
        ] = f"inline; filename=Invoice_no_{invoice.invoice_no}.pdf"
    return response


@app.route("/user_data", methods=["GET", "POST"])
@login_required
def user_data():
    user = User.query.get_or_404(current_user.id)
    if request.method == "POST":
        user.id = user.id
        user.email = user.email
        user.name = user.name
        user.surname = user.surname
        user.phone_no = user.phone_no
        user.password = user.password
        user.company_name = user.company_name
        user.street = user.street
        user.house_no = user.house_no
        user.flat_no = user.flat_no
        user.zip_code = user.zip_code
        user.city = user.city
        user.tax_no = user.tax_no
        user.bank_account = user.bank_account
        return redirect(url_for("user_data_edit"))
    return render_template("user_data.html", user=user)


@app.route("/user_data_edit", methods=["GET", "POST"])
@login_required
def user_data_edit():
    user = User.query.get_or_404(current_user.id)
    if request.method == "POST":
        user.id = user.id
        user.email = user.email
        user.name = user.name
        user.surname = user.surname
        user.phone_no = request.form.get("phone_no")
        user.password = request.form.get("password")
        user.company_name = request.form.get("company_name")
        user.street = request.form.get("street")
        user.house_no = request.form.get("house_no")
        user.flat_no = request.form.get("flat_no")
        user.zip_code = request.form.get("zip_code")
        user.city = request.form.get("city")
        user.tax_no = request.form.get("tax_no")
        user.bank_account = request.form.get("bank_account")
        try:
            db_session.commit()
            return redirect(url_for("user"))
        except SQLAlchemyError:
            print("There was an error.")
    return render_template("user_data_edit.html", user=user, is_edit=True)


@app.route("/your_invoices/send_email/<int:id>", methods=["GET", "POST"])
@login_required
def send_invoice_as_attachment(id):
    invoice = InvoiceForm.query.get_or_404(id)
    user = User.query.filter(invoice.issuer_id == User.id).first()
    recipient = Contractor.query.filter(invoice.recipient_id == Contractor.id).first()
    if request.method == "POST":
        send_email(
            id=invoice.id,
            sender_address=request.form.get("issuer_email") or user.email,
            sender_pass=credentials["MAIL_PASSWORD"],
            receiver_address=request.form.get("recipient_email"),
            subject=request.form.get("subject"),
            body=request.form.get("email_body"),
            filename=f"{credentials['PATH_TO_DOWNLOAD_FOLDER']}/Invoice_no_{invoice.invoice_no}.pdf",
        )
        return redirect(url_for("your_invoices"))
    return render_template(
        "send_email.html", invoice=invoice, user=user, recipient=recipient
    )


def send_email(
    sender_address,
    sender_pass,
    receiver_address,
    subject,
    body,
    filename=None,
    id=None,
):
    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    # The subject line
    message["Subject"] = subject
    # The body and the attachments for the mail
    message.attach(MIMEText(body, "plain"))

    if filename is not None and id is not None:
        if os.path.exists(f"{credentials['PATH_TO_DOWNLOAD_FOLDER']}/{filename}"):
            os.remove()
        show_pdf(id=id, download=True)
        attach_file = open(filename, "rb")  # Open the file as binary mode
        # os search filename in downloads and remove
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header("Content-Decomposition", "attachment", filename=filename)
        message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP(credentials["MAIL_SERVER"], credentials["MAIL_PORT"])
    # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


if __name__ == "__main__":
    app.run(debug=True)
