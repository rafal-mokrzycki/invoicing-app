""" to run: python -m pytest -vv tests\test_credentials.py -s
add --pdb to debug in command line
use VScode test tools recommended (the beaker) """
import os
import unittest

import pandas as pd
import pytest
import repackage

# from src.utils.utils import addValues, confirm_user_choice

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


def fake_input_default_email_server(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL_SERVER}) or hit ENTER to leave {DEFAULT_EMAIL_SERVER}): ": DEFAULT_EMAIL_SERVER
    }
    return prompt_to_return_val[the_prompt]


def fake_input_correct_email_server(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL_SERVER}) or hit ENTER to leave {DEFAULT_EMAIL_SERVER}): ": "correct.email.srv"
    }
    return prompt_to_return_val[the_prompt]


def fake_input_wrong_email_server(the_prompt):
    prompt_to_return_val = {
        f"Type in your email (eg. {DEFAULT_EMAIL_SERVER}) or hit ENTER to leave {DEFAULT_EMAIL_SERVER}): ": "wrongemailserver"
    }
    return prompt_to_return_val[the_prompt]


def test_get_and_check_email_default(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_default_email)
    assert get_and_check_email() == DEFAULT_EMAIL


def test_get_and_check_email_correct(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_correct_email)
    assert get_and_check_email() == "correct@email.address"


def test_get_and_check_email_wrong(monkeypatch):
    pass
    #     monkeypatch.setattr("builtins.input", fake_input_wrong_email)
    #     assert get_and_check_email() == "Wrong email format. Try again."


def test_get_and_check_password_correct():
    pass


def test_get_and_check_password_wrong():
    pass


def test_get_mail_server_default(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_default_email_server)
    assert get_mail_server() == DEFAULT_EMAIL_SERVER


def test_get_mail_server_correct(monkeypatch):
    monkeypatch.setattr("builtins.input", fake_input_correct_email_server)
    assert get_mail_server() == "correct.email.srv"


def test_get_mail_server_wrong(monkeypatch):
    pass


def test_get_db_secret_key_default():
    pass


def test_get_db_secret_key_correct():
    pass


def test_get_db_secret_key_wrong():
    pass


if __name__ == "__main__":
    pass
    print(get_db_secret_key())
