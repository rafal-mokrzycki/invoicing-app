#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""

import numpy as np
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config_files.config import credentials, settings
from scripts.database import Invoice

app = Flask(__name__)
app.config.update(credentials)

db = SQLAlchemy(app)


CURRENCY = settings["CURRENCY"]


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

    def __repr__(self):
        return "<Invoice %r>" % self.id


def format_percentages(number):
    """Formats a floating point number into string, i.e. 0.23 -> '23%'"""
    return str(int(number * 100)) + "%"


def format_number(number):
    """Formats a floating point number into string iwht a currency code, i.e. 2.50 -> '2.50 PLN'"""
    return "{:.2f}".format(number) + f" {CURRENCY}"


def get_number_of_invoices_in_db():
    return db.session.query(InvoiceForm).count() + 1
