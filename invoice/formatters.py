#!/usr/bin/env python
"""
Format functions
"""

CURRENCY = "PLN"


def format_percentages(number: float):
    """Formats a floating point number into string, i.e. 0.23 -> '23%'

    Args:
        number (float): A float to be formatted.

    Returns:
        str: Formatted string in format eg. 23%.
    """
    return str(int(number * 100)) + "%"


def format_number(number: float, currency: str = CURRENCY):
    """Formats a floating point number into string wiht a currency code,
    i.e. 2.50 -> '2.50 PLN'

    Args:
        number (float): A float to be formatted.
        currency (str, optional): _description_. Defaults to CURRENCY.

    Returns:
        str: Formatted string in format eg. 2.50 PLN.
    """
    return "{:.2f}".format(number) + f" {currency}"


def format_bank_account():
    pass
