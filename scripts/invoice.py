#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""
import datetime

import numpy as np
from config_files.config import config
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)


CURRENCY = config["CURRENCY"]


class Invoice(db.Model, UserMixin):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    invoice_no = db.Column(db.String(250), nullable=False)
    invoice_type = db.Column(db.String(250), nullable=False)
    issue_city = db.Column(db.String(250), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    issuer_tax_no = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    price_net = db.Column(db.Float, nullable=False)
    recipient_tax_no = db.Column(db.Integer, nullable=False)
    sell_date = db.Column(db.Date, nullable=False)
    sum_gross = db.Column(db.Float, nullable=False)
    sum_net = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(250), nullable=False)

    def __init__(
        self,
        id,
        amount,
        invoice_no,
        invoice_type,
        issue_city,
        issue_date,
        issuer_tax_no,
        position,
        price_net,
        recipient_tax_no,
        sell_date,
        sum_gross,
        sum_net,
        tax_rate,
        unit,
    ):
        self.id = id
        self.invoice_no = invoice_no
        self.invoice_type = invoice_type
        self.issue_city = issue_city
        self.issue_date = issue_date
        self.issuer_tax_no = issuer_tax_no
        self.position = position
        self.price_net = price_net
        self.recipient_tax_no = recipient_tax_no
        self.sell_date = sell_date
        self.sum_gross = sum_gross
        self.sum_net = sum_net
        self.tax_rate = tax_rate
        self.unit = unit
        self.amount = amount

    def __repr__(self):
        return "<Invoice %r>" % self.id


def calculate_gross(amount, tax_rate):
    if tax_rate in config["TAX_RATES"]:
        return float(amount + amount * tax_rate)
    else:
        raise ValueError("Wrong tax rate")


def calculate_sum(iterable):
    return float(np.sum(iterable))


def format_percentages(number):
    return str(int(number * 100)) + "%"


def format_number(number):
    return "{:.2f}".format(number) + f" {CURRENCY}"


def get_number_of_invoices_in_db():
    return db.session.query(Invoice).count() + 1


def ceidg_api():
    pass
