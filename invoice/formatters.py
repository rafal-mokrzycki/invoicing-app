#!/usr/bin/env python
"""
Format functions
"""

CURRENCY = "PLN"


def format_percentages(number):
    """Formats a floating point number into string, i.e. 0.23 -> '23%'"""
    return str(int(number * 100)) + "%"


def format_number(number):
    """Formats a floating point number into string wiht a currency code,
    i.e. 2.50 -> '2.50 PLN'"""
    return "{:.2f}".format(number) + f" {CURRENCY}"
