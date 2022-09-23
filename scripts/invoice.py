#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""

import numpy as np
from config_files.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from scripts.database import Invoice

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)


CURRENCY = config["CURRENCY"]


class InvoiceForm(Invoice):
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
    return db.session.query(InvoiceForm).count() + 1


def ceidg_api():
    pass
