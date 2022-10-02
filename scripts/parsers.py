#!/usr/bin/env python
"""
Parsers
"""
import calendar
import datetime
import json

import repackage

# from config_files.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

repackage.up()
from config_files.config import config

from scripts.invoice import InvoiceForm

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)


def parse_invoice_number(invoice_type):
    """
    Takes invoice type andbased on the current year and month, number of invoices in DB
    and pattern YYYY/MM/number_of_invoice parses invoice number.
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
        db.session.query(InvoiceForm.invoice_type, func.count(InvoiceForm.invoice_type))
        .group_by(InvoiceForm.invoice_type)
        .filter(InvoiceForm.issue_date > last_day_of_previous_month)
        .filter(InvoiceForm.issue_date < first_day_of_next_month)
        .all()
    )
    try:
        invoice_number = [elem[1] for elem in query if elem[0] == invoice_type][0]
    except IndexError:
        invoice_number = 1
    return f"{current_year}/{current_month}/{invoice_number + 1}"


def parse_json_with_invoices_counted(write_json=True):
    """
    Takes invoice type andbased on the current year and month, number of invoices in DB
    and return json with invoices counted by groups for a given month.
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
    query = (
        db.session.query(InvoiceForm.invoice_type, func.count(InvoiceForm.invoice_type))
        .group_by(InvoiceForm.invoice_type)
        .filter(InvoiceForm.issue_date > last_day_of_previous_month)
        .filter(InvoiceForm.issue_date < first_day_of_next_month)
    )
    if write_json:
        with open("invoices_counted.json", "w") as f:
            f.write(json.dumps(dict(query)))
    elif len(dict(query)) < 3:
        return {"regular": "13", "proforma": "21", "advanced_payment": "2"}
    else:
        return json.dumps(dict(query))


invoice_number_on_type = parse_json_with_invoices_counted(False)
print(invoice_number_on_type["regular"])
