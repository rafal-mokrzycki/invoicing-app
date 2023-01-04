#!/usr/bin/env python
"""
Helper functions
"""
import json
import os
import time
from sqlite3 import Connection

import pandas as pd
import repackage
from IPython.display import clear_output


def append_dict(dict1: dict, dict2: dict):
    """Appends one dictionary to another one keeping keys from both
    and returning a sum of their values as strings.

    Args:
        dict1 (dict): Dictionary to append to.
        dict2 (dict): Dictionary to append.

    Returns:
        dict: Result dictionary.
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


def get_currencies(
    filename="currencies.csv", columns: list = None, filepath: str = None
):
    """Reads the CSV file with currency symbols and parses them to UI.

    Args:
        filename (str, optional): File where info about currencies is stored.
        Defaults to "currencies.csv".
        columns (list, optional): List of columns to use. Defaults to None.
        filepath (str, optional): Filepath to the file where info about
        currencies is stored. Defaults to None.

    Returns:
        list: List of currencies.
    """

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


def get_number_of_objects_in_table(
    database: Connection = None, table: str = None, object: str = None
):
    """Return number of invoices by type.

    Args:
        database (Connection, optional): Connection to the database.
        Defaults to None.
        table (str, optional): Table name. Defaults to None.
        object (str, optional): Variable name. Defaults to None.

    Returns:
        dict: Dictionary with invoice names and count of each type.
    """

    query = f"""
    SELECT {object}, count({object})
    AS count FROM {table}
    GROUP BY {object};
    """
    list_of_tuples = [tuple(row) for row in database.execute(query).fetchall()]
    return {elem[0]: elem[1] for elem in list_of_tuples}


def wait(step: int = 1, max: int = 3, string: str = "Processing"):
    """_summary_

    Args:
        step (int, optional): Length of time between steps. Defaults to 1.
        max (int, optional): Number of seconds to wait for. Defaults to 3.
        string (str, optional): String to be displayed in each step.
        Defaults to "Processing".
    """
    for x in range(0, max):
        display = string + "." * (x + 1)
        print(display, end="\r")
        time.sleep(step)
    clear_output(wait=True)
