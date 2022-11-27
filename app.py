#!/usr/bin/env python
"""
To run type: flask --app hello run
"""
import datetime
import os
import smtplib
import sqlite3
import sys
import time
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import repackage

repackage.up(1)
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
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from config_files.config import credentials, settings

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.update(credentials)
mail = Mail(app)
db = SQLAlchemy(app)
Base = declarative_base()
engine = create_engine(
    "sqlite:///database.db",
    # connect_args={"port": 3306},
    # echo="debug",
    # echo_pool=True,
)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


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


class Invoice(Model, UserMixin, Base):
    """
    A class used to represent an Invoice. Inherits from Model, UserMixin and Base.
    Attributes
    ----------
    __tablename__ : str
        default="invoices"
    id : int
        primary key
    amount : float
        amount of goods in an item
    invoice_no : str
        invoice number, set automatically
    invoice_type : str
        invoice type, one of the following: "regular", "advanced payment", "proforma"
    issue_city : str
        issue city
    issue_date : date
        issue date
    issuer_tax_no : int
        issuer tax number
    item : str
        item / position
    price_net : float
        price net of a good
    recipient_tax_no : int
        recipient tax number
    sell_date : date
        sell date
    sum_gross : float
        sum gross (sum of all goods in an item * tax rate)
    sum_net : float
        sum net (sum of all goods in an item)
    tax_rate : float
        tax rate for an item, one of the following: 0.00, 0.05, 0.08, 0.23
    unit : str
        unit of an item
    currency : str
        currency of an item
    issuer_id : int
        issuer id, foreign key
    recipient_id : int
        recipient id, foreign key
    """

    __tablename__ = settings["TABLE_NAMES"][2]
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    invoice_no = Column(String(250), nullable=False)
    invoice_type = Column(String(250), nullable=False)
    issue_city = Column(String(250), nullable=False)
    issue_date = Column(Date, nullable=False)
    issuer_tax_no = Column(Integer, nullable=False)
    item = Column(String(250), nullable=False)
    price_net = Column(Float, nullable=False)
    recipient_tax_no = Column(Integer, nullable=False)
    sell_date = Column(Date, nullable=False)
    sum_gross = Column(Float, nullable=False)
    sum_net = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
    unit = Column(String(250), nullable=False)
    currency = Column(String(250), nullable=False)
    issuer_id = Column(Integer, ForeignKey("accounts.id"))
    recipient_id = Column(Integer, ForeignKey("contractors.id"))


class User(Model, UserMixin, Base):
    """
    A class used to represent a User. Inherits from Model, UserMixin and Base.
    Attributes
    ----------
    __tablename__ : str
        default="accounts"
    id : int
        primary key
    email : str
        email
    name : str
        first name
    surname : str
        last name
    phone_no  : int
        phone number
    password : str
        password
    company_name  : str
        company name
    street  : str
        street
    house_no : int
        house number
    flat_no : int
        flat number
    zip_code  : str
        zip code
    city : str
        city
    tax_no : int
        tax number
    bank_account : int
        tax number
    plan : str
        plan for the account, one from the following: "free", "starter", "business", "ultimate"
    terms : bool
        if the user agreed to the terms of use
    newsletter : bool
        if the user wants to receive a newsletter
    """

    __tablename__ = settings["TABLE_NAMES"][0]
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    phone_no = Column(Integer, nullable=False)
    password = Column(String(250), nullable=False)
    company_name = Column(String(250), nullable=True)
    street = Column(String(250), nullable=True)
    house_no = Column(String(250), nullable=True)
    flat_no = Column(String(250), nullable=True)
    zip_code = Column(String(250), nullable=True)
    city = Column(String(250), nullable=True)
    tax_no = Column(String(250), nullable=True)
    bank_account = Column(String(250), nullable=True)
    plan = Column(String(250), nullable=False)
    terms = Column(Boolean, nullable=False)
    newsletter = Column(Boolean, nullable=False)


class Contractor(Model, UserMixin, Base):
    """
    A class used to represent a User. Inherits from Model, UserMixin and Base.
    Attributes
    ----------
    __tablename__ : str
        default="accounts"
    id : int
        primary key
    email : str
        email
    name : str
        first name
    surname : str
        last name
    phone_no  : int
        phone number
    company_name  : str
        company name
    street  : str
        street
    house_no : int
        house number
    flat_no : int
        flat number
    zip_code  : str
        zip code
    city : str
        city
    tax_no : int
        tax number
    bank_account : int
        tax number
    """

    __tablename__ = settings["TABLE_NAMES"][1]
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=True)
    name = Column(String(250), nullable=True)
    surname = Column(String(250), nullable=True)
    phone_no = Column(Integer, nullable=True)
    company_name = Column(String(250), nullable=True)
    street = Column(String(250), nullable=True)
    house_no = Column(String(250), nullable=True)
    flat_no = Column(String(250), nullable=True)
    zip_code = Column(String(250), nullable=True)
    city = Column(String(250), nullable=True)
    tax_no = Column(String(250), nullable=True)
    bank_account = Column(String(250), nullable=True)


if __name__ == "__main__":
    app.run(debug=True)
