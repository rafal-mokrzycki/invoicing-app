#!/usr/bin/env python
"""
Parsers
"""
import calendar
import datetime

import pandas as pd
import repackage
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

repackage.up()
from config_files.config import credentials, settings

from scripts.invoice import InvoiceForm

app = Flask(__name__)
app.config.update(credentials)

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


def parse_dict_with_invoices_counted():
    """
    Takes invoice type andbased on the current year and month, number of invoices in DB
    and return json with invoices counted by groups for a given month.
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
        db.session.query(InvoiceForm.invoice_type, func.count(InvoiceForm.invoice_type))
        .group_by(InvoiceForm.invoice_type)
        .filter(InvoiceForm.issue_date > last_day_of_previous_month)
        .filter(InvoiceForm.issue_date < first_day_of_next_month)
    )
    return append_dict(empty_dict, dict(query))


def append_dict(dict1, dict2):
    """
    Appends one dictionary to another one keeping keys from both and returning
    a sum of their values.
    """
    result = {}
    for i in set(list(dict1.keys()) + list(dict2.keys())):
        if i not in dict1:
            result[i] = dict2[i]
        elif i not in dict2:
            result[i] = dict1[i]
        else:
            result[i] = dict1[i] + dict2[i]
    for key in result:
        result[key] = str(result[key])
    return result


def parse_currencies(filename='currencies.csv', columns=['Currency Code']):
    """
    Reads the CSV file with currency symbols and parses them to UI
    """
    filepath = repackage.add(f'../config_files/{filename}')
    df = pd.read_csv(filepath)
    df1 = df[df['Currency Code'].isin(['PLN','EUR','USD','GBP','JPY'])]
    df2 = df[~df1]
    if len(columns) == 1:
        result = [df1[columns[0]].values, df2[columns[0]].values]
    result = [df1[columns].values, df2[columns].values]
    return result


print(parse_currencies())
