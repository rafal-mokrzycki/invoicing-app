#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""
import datetime as dt
import logging
import random
import smtplib
from pathlib import Path

import numpy as np
import pandas as pd
from config_files.config import config
from fpdf import FPDF


class InvoiceCreator:
    def __init__(
        self,
        invoice_type,
        issuer_tax_no,
        recipient_tax_no,
        positions,
        prices_net,
        tax_rates,
    ):
        if invoice_type in config["INVOICE_TYPES"]:
            self.invoice_type = invoice_type
        else:
            raise ValueError("Wrong invoice type")
        self.issuer_tax_no = issuer_tax_no
        self.recipient_tax_no = recipient_tax_no
        self.positions = positions
        self.prices_net = prices_net
        self.tax_rates = tax_rates
        self.prices_gross = [
            calculate_gross(i, j) for i, j in zip(self.prices_net, self.tax_rates)
        ]
        self.sum_net = calculate_sum(self.prices_net)
        self.sum_gross = calculate_sum(self.prices_gross)
        self.sum_tax = self.sum_gross - self.sum_net

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
        # {[(i, j, k, l) for i, j, k, l in zip(self.positions, self.prices_net, self.tax_rates, self.prices_gross)]}
        # """
        string3 = f"""
        Net sum: {self.sum_net}
        Tax sum: {self.sum_tax}
        TOTAL SUM: {self.sum_gross}
        {'='*60}"""

        print(string1, string2, string3, sep="\n\n")

    def save_to_pdf(self):
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page()
        pdf.set_font("Times", "", 12)
        pdf.cell(200, 10, txt="Hey", ln=2, align="C")
        pdf.output("GFG.pdf")


def calculate_gross(amount, tax_rate):
    if tax_rate in config["TAX_RATES"]:
        return amount + amount * tax_rate
    else:
        raise ValueError("Wrong tax rate")


def calculate_sum(iterable):
    return np.sum(iterable)
