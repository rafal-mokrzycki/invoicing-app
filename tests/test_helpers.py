""" to run: python -m pytest -vv tests\test_helpers.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker) """
import os

import pandas as pd
import pytest
import repackage

repackage.up()
from invoice.helpers import (
    add_country_code,
    append_dict,
    get_currencies,
    split_whitespaces,
    validate_bank_account,
)


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


# @pytest.fixture(scope="module", name="bank_account_right")
# def fixture_bank_account_right():
#     yield ""


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


def test_validate_bank_account_right():
    pass


def test_validate_bank_account_wrong():
    pass


def test_split_whitespaces():
    string = "a sd asd asdasd"
    assert split_whitespaces(string) == "asdasdasdasd"


def test_add_whitespaces():
    pass


def test_add_country_code():
    string = "1234"
    code = "EN"
    assert add_country_code(string, code) == "EN1234"


validate_bank_account("65 1060 0076 0000 3200 0005 7153")
