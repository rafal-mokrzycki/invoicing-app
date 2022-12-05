""" to run: python -m pytest -vv tests\test_helpers.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker) """
import os

import pandas as pd
import pytest
import repackage

repackage.up(2)
from scripts.helpers import append_dict, get_currencies


@pytest.fixture(scope="module", name="dictionary_left")
def fixture_dictionary_left():
    dictionary = {
        "A": 1,
        "B": 2,
    }

    yield dictionary


@pytest.fixture(scope="module", name="dictionary_right")
def fixture_dictionary_right():
    dictionary = {
        "A": 2,
        "C": 4,
    }

    yield dictionary


def test_get_currencies():
    df = pd.DataFrame({"Currency": ["PLN", "EUR", "USD", "GBP", "JPY"]})
    df.to_csv("csvfile.csv", index=False)
    assert get_currencies("csvfile.csv", "Currency", "csvfile.csv") == [
        ["PLN", "EUR", "USD", "GBP", "JPY"],
        [],
    ]
    os.remove("csvfile.csv")


def test_append_dict(dictionary_left, dictionary_right):
    result = {"A": "3", "B": "2", "C": "4"}
    assert append_dict(dictionary_left, dictionary_right) == result
