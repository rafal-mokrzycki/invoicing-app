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

# repackage.up(2)
# from app import db


db = SQLAlchemy()


class Invoice(db.Model, UserMixin):
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
    # issuer_id = Column(Integer, ForeignKey("accounts.id"))
    # recipient_id = Column(Integer, ForeignKey("contractors.id"))


class InvoiceForm(Invoice):
    """
    A class used to represent an Invoice. Inherits from Invoice.
    Attributes
    ----------
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
    Methods
    ----------
    __repr__()
        Returns invoice id
    """

    def __init__(
        self,
        id,
        amount,
        invoice_no,
        invoice_type,
        issue_city,
        issue_date,
        issuer_tax_no,
        item,
        price_net,
        recipient_tax_no,
        sell_date,
        sum_gross,
        sum_net,
        tax_rate,
        unit,
        currency,
        # issuer_id,
        # contractor_id,
    ):
        super().__init__()
        self.id = id
        self.invoice_no = invoice_no
        self.invoice_type = invoice_type
        self.issue_city = issue_city
        self.issue_date = issue_date
        self.issuer_tax_no = issuer_tax_no
        self.item = item
        self.price_net = price_net
        self.recipient_tax_no = recipient_tax_no
        self.sell_date = sell_date
        self.sum_gross = sum_gross
        self.sum_net = sum_net
        self.tax_rate = tax_rate
        self.unit = unit
        self.amount = amount
        self.currency = currency
        # self.issuer_id = issuer_id
        # self.contractor_id = contractor_id

    def __repr__(self):
        return "<Invoice %r>" % self.id

    def get_invoice_number(self, invoice_type):
        """Takes invoice type and gets invoice number based on the current year and month,
        number of invoices in DB and pattern YYYY/MM/number_of_invoice.
        """
        current_date = datetime.date.today()
        last_day_of_previous_month = datetime.date(
            current_date.year,
            current_date.month - 1,
            calendar.monthrange(current_date.year, current_date.month - 1)[1],
        )
        first_day_of_next_month = datetime.date(
            current_date.year,
            current_date.month + 1,
            1,
        )
        current_year = datetime.datetime.now().strftime("%Y")
        current_month = datetime.datetime.now().strftime("%m")
        query = (
            db_session.query(self.invoice_type, func.count(self.invoice_type))
            .group_by(self.invoice_type)
            .filter(self.issue_date > last_day_of_previous_month)
            .filter(self.issue_date < first_day_of_next_month)
            .all()
        )
        try:
            invoice_number = [elem[1] for elem in query if elem[0] == invoice_type][0]
        except IndexError:
            invoice_number = 1
        return f"{current_year}/{current_month}/{invoice_number + 1}"


def get_dict_with_invoices_counted(object):
    """Takes invoice type and based on the current year and month,
    number of invoices in DB, returns a JSON file with invoices
    counted by groups for a given month.
    """
    empty_dict = {
        [i for i in settings["INVOICE_TYPES"]][i]: [
            1 for _ in range(len(settings["INVOICE_TYPES"]))
        ][i]
        for i in range(len([i for i in settings["INVOICE_TYPES"]]))
    }
    current_date = datetime.date.today()
    last_day_of_previous_month = datetime.date(
        current_date.year,
        current_date.month - 1,
        calendar.monthrange(current_date.year, current_date.month - 1)[1],
    )
    first_day_of_next_month = datetime.date(
        current_date.year,
        current_date.month + 1,
        1,
    )
    query = (
        db_session.query(object.invoice_type, func.count(object.invoice_type))
        .group_by(object.invoice_type)
        .filter(object.issue_date > last_day_of_previous_month)
        .filter(object.issue_date < first_day_of_next_month)
    )
    return append_dict(empty_dict, dict(query))


class User(db.Model, UserMixin):
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
        plan for the account, one from the following:
        "free", "starter", "business", "ultimate"
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

    def __init__(
        self,
        # id,
        email,
        name,
        surname,
        phone_no,
        password,
        # company_name,
        # street,
        # house_no,
        # flat_no,
        # zip_code,
        # city,
        # tax_no,
        # bank_account,
        plan,
        terms,
        newsletter,
    ):
        self.id = db_session.query(User).count()
        self.email = email
        self.name = name
        self.surname = surname
        self.phone_no = phone_no
        self.password = password
        # self.company_name = company_name
        # self.street = street
        # self.house_no = house_no
        # self.flat_no = flat_no
        # self.zip_code = zip_code
        # self.city = city
        # self.tax_no = tax_no
        # self.bank_account = bank_account
        self.plan = plan
        self.terms = terms
        self.newsletter = newsletter


class Contractor(db.Model, UserMixin):
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
