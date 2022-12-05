""" to run: python -m pytest -vv tests\test_credentials.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker) """
import os

import pandas as pd
import pytest
import repackage

repackage.up()
from scripts.credentials import (
    DEFAULT_EMAIL,
    DEFAULT_EMAIL_SERVER,
    DEFAULT_PASSWORD,
    get_and_check_email,
    get_and_check_password,
    get_db_secret_key,
    get_mail_server,
    update_credentials,
)


def fake_input_default_email(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL}) or hit ENTER to leave {DEFAULT_EMAIL}): ": DEFAULT_EMAIL
    }
    return prompt_to_return_val[the_prompt]


def fake_input_correct_email(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL}) or hit ENTER to leave {DEFAULT_EMAIL}): ": "correct@email.address"
    }
    return prompt_to_return_val[the_prompt]


def fake_input_wrong_email(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL}) or hit ENTER to leave {DEFAULT_EMAIL}): ": "wrong.email"
    }
    return prompt_to_return_val[the_prompt]


def test_get_and_check_email_default(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_default_email)
    assert get_and_check_email() == DEFAULT_EMAIL


def test_get_and_check_email_correct(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_correct_email)
    assert get_and_check_email() == "correct@email.address"


def test_get_and_check_email_wrong(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_wrong_email)
    while True:
        assert get_and_check_email() == "Wrong email format. Try again."
        break


# def test_get_and_check_password_different():
#     pass


# def test_get_and_check_email_normal_input():
#     assert get_and_check_email("mail@user.name") == "mail@user.name"


# def test_get_and_check_email_wrong_input():
#     assert get_and_check_email("") == DEFAULT_EMAIL

if __name__ == "__main__":
    print(get_and_check_email())
