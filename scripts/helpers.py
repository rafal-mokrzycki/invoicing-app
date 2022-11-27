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

app = Flask(__name__)
app.config.update(credentials)

db = SQLAlchemy(app)


def append_dict(dict1, dict2):
    """Appends one dictionary to another one keeping keys from both and returning
    a sum of their values as strings.
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


def get_currencies(filename="currencies.csv", columns=None, filepath=None):
    """Reads the CSV file with currency symbols and parses them to UI"""

    if columns is None:
        columns = ["Currency Code"]
    if filepath is None:
        filepath = repackage.add(f"../config_files/{filename}")
    df = pd.read_csv(filepath)
    df_selected = df[~df[columns].isin(["PLN", "EUR", "USD", "GBP", "JPY"])]
    if len(columns) == 1:
        return [
            ["PLN", "EUR", "USD", "GBP", "JPY"],
            df_selected[columns[0]].values.tolist(),
        ]
    else:
        return [
            ["PLN", "EUR", "USD", "GBP", "JPY"],
            df_selected[columns].values.tolist(),
        ]
