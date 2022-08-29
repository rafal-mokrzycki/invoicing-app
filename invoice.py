#!/usr/bin/env python
"""
Utilities to create a new ivoice
"""


class InvoiceCreator:
    def __init__(self, invoice_type, issuer_tax_no, recipient_tax_no) -> None:
        self.invoice_type = invoice_type
        self.issuer_tax_no = issuer_tax_no
        self.recipient_tax_no = recipient_tax_no


def count_gross(amount, tax_rate):
    return amount * tax_rate
