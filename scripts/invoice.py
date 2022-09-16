#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""
import datetime

import numpy as np
from config_files.config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)


CURRENCY = config["CURRENCY"]


class Invoice(db.Model):
    __tablename__ = "invoices"
    invoice_no = db.Column(db.String(250), primary_key=True)
    invoice_type = db.Column(db.String(250), nullable=False)
    issue_date = db.Column(db.String(250), nullable=False)
    issue_city = db.Column(db.String(250), nullable=False)
    sell_date = db.Column(db.String(250), nullable=False)
    issuer_tax_no = db.Column(db.Integer, nullable=False)
    recipient_tax_no = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(250), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(250), nullable=False)
    price_net = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    sum_net = db.Column(db.Float, nullable=False)
    sum_gross = db.Column(db.Float, nullable=False)

    def __init__(
        self,
        invoice_type,
        invoice_no,
        issue_date,
        issue_city,
        sell_date,
        issuer_tax_no,
        recipient_tax_no,
        position,
        amount,
        unit,
        price_net,
        tax_rate,
        sum_net,
        sum_gross,
    ):
        self.invoice_type = invoice_type
        self.invoice_no = invoice_no
        self.issue_date = issue_date
        self.issue_city = issue_city
        self.sell_date = sell_date
        self.issuer_tax_no = issuer_tax_no
        self.recipient_tax_no = recipient_tax_no
        self.position = position
        self.amount = amount
        self.unit = unit
        self.price_net = price_net
        self.tax_rate = tax_rate
        self.sum_net = sum_net
        self.sum_gross = sum_gross

    def show_invoice(self):
        string1 = f"""
        {'='*60}
        {self.invoice_type.upper()} INVOICE

        Issuer tax no.: {self.issuer_tax_no}
        Recipient tax no.: {self.recipient_tax_no}

        Position\tNet amount\tTax rate\tGross amount
        """
        string2 = ""
        # string2 = f"""

        # {[(i, j, k, l) for i, j, k, l in zip(self.position, self.price_net, self.tax_rate, self.price_gross)]}

        # """
        string3 = f"""
        Net sum: {self.sum_net}
        Tax sum: {self.sum_tax}
        TOTAL SUM: {self.sum_gross}
        {'='*60}"""

        print(string1, string2, string3, sep="\n\n")

    def save_to_pdf(self):
        """Saves invoice as a pdf file"""

        # tax_rate_to_print = [str(int(i * 100), "%") for i in self.tax_rate]
        tax_rate_to_print = [format_percentages(i) for i in self.tax_rate]
        price_net_to_print = [format_number(i) for i in self.price_net]
        price_gross_to_print = [format_number(i) for i in self.price_gross]

        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()

        # Set invoice name
        pdf.set_font("Times", "B", 16)
        pdf.cell(0, 16, txt=f"{self.invoice_type.upper()} INVOICE", ln=2, align="L")

        # Issuer and recipient data
        pdf.set_font("Times", "", 12)
        pdf.cell(200, 10, txt=f"Issuer tax no.: {self.issuer_tax_no}", ln=2, align="l")
        pdf.cell(
            200, 10, txt=f"Recipient tax no.: {self.recipient_tax_no}", ln=2, align="l"
        )

        # position of an invoice

        pdf.set_font("Times", "B", 12)
        for size, elem in zip(
            [100, 30, 30, 30], ["Position", "Net amount", "Tax rate", "Gross amount"]
        ):
            pdf.cell(size, 8, txt=elem, ln=0, border=1)
        pdf.cell(10, 8, txt="", ln=1)
        pdf.set_font("Times", "", 12)

        for position in range(len(self.position)):
            for size, elem in zip(
                [100, 30, 30, 30],
                [
                    self.position,
                    price_net_to_print,
                    tax_rate_to_print,
                    price_gross_to_print,
                ],
            ):
                pdf.cell(size, 10, txt=str(elem[position]), ln=0, border=1)
            pdf.cell(10, 10, txt="", ln=1)

        # Net, tax and gross amount
        pdf.cell(200, 10, txt=f"Net sum: {self.sum_net} {CURRENCY}", ln=2, align="R")
        pdf.cell(200, 10, txt=f"Tax sum: {self.sum_tax} {CURRENCY}", ln=2, align="R")
        pdf.set_font("Times", "B", 12)
        pdf.cell(200, 10, txt=f"TOTAL SUM: {self.sum_gross} {CURRENCY}", ln=2, align="R")

        pdf.output(
            f"{self.invoice_type.replace(' ','_')}_invoice_{datetime.datetime.now().strftime('%Y%m%d')}.pdf"
        )


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


def get_new_invoice_number():
    return datetime.datetime.now().strftime(f"%Y/%m/1")  # TODO: invoices database


def ceidg_api():
    pass
