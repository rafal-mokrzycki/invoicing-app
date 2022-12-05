#!/usr/bin/env python
"""to run: python -m create_database.py"""
import json
import os
from getpass import getpass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
import repackage

repackage.up()
from scripts.validators import Validator

# https://deniscapeto.com/2021/03/06/how-to-test-a-while-true-in-python/
DEFAULT_EMAIL = "example@example.com"
DEFAULT_EMAIL_SERVER = "smtp.example.com"
DEFAULT_PASSWORD = "example"


def update_credentials():
    """Takes Credentials class attributes and saves them to credentials.json."""
    json_path = os.path.join("config_files", "credentials.json")
    csv_path = os.path.join("config_files", "demo_accounts.csv")
    data = {}
    data["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    data["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    data["MAIL_PORT"] = 587
    data["MAIL_USERNAME"] = get_and_check_email() or DEFAULT_EMAIL
    data["MAIL_PASSWORD"] = get_and_check_password() or DEFAULT_PASSWORD
    data["MAIL_SERVER"] = get_mail_server() or DEFAULT_EMAIL_SERVER
    data["SECRET_KEY"] = get_db_secret_key() or DEFAULT_PASSWORD
    data["MAIL_USE_TLS"] = True
    data["MAIL_USE_SSL"] = False
    data["PATH_TO_DOWNLOAD_FOLDER"] = str(os.path.join(Path.home(), "Downloads"))
    with open(json_path, "w") as jsonFile:
        json.dump(data, jsonFile)
    df = pd.read_csv(csv_path)
    df["email"].iloc[0] = data["MAIL_USERNAME"]
    df["password"].iloc[0] = data["MAIL_PASSWORD"]
    df.to_csv(csv_path, index=None)
    print(
        f"""
Your credentials were set to the following and saved in {json_path} file:

{'='*100}
||  'SECRET_KEY': {'(empty)' if ' ' else data["SECRET_KEY"]}
||  'SQLALCHEMY_DATABASE_URI': {data["SQLALCHEMY_DATABASE_URI"]}
||  'SQLALCHEMY_TRACK_MODIFICATIONS': {data["SQLALCHEMY_TRACK_MODIFICATIONS"]}
||  'MAIL_SERVER': {data["MAIL_SERVER"]}
||  'MAIL_PORT': {data["MAIL_PORT"]}
||  'MAIL_USERNAME': {data["MAIL_USERNAME"]}
||  'MAIL_PASSWORD': {'(empty)' if ' ' else data["MAIL_PASSWORD"]}
||  'MAIL_USE_TLS': {data["MAIL_USE_TLS"]}
||  'MAIL_USE_SSL': {data["MAIL_USE_SSL"]}
||  'PATH_TO_DOWNLOAD_FOLDER': {data["PATH_TO_DOWNLOAD_FOLDER"]}
{'='*100}

You can change the settings anytime by updating the {json_path} file.
"""
    )


def get_and_check_email(
    mail_username: str = None, responses: Optional[Iterable[str]] = None
):
    """Return a valid email address based on user input."""
    if responses is None:
        # An infinite stream of calls to input()
        responses = iter(
            lambda: input(
                f"Type in your email (eg. {DEFAULT_EMAIL}) or hit ENTER to leave {DEFAULT_EMAIL}): "
            ),
            None,
        )

    for mail_username in responses:
        if Validator().validate_email_address(mail_username):
            return mail_username
        elif mail_username == "":
            return DEFAULT_EMAIL
        else:
            print("Wrong email format. Try again.")
    else:
        # Note: cannot be raised from the default value of responses
        raise ValueError("Unexpected end of responses")


def get_and_check_password():
    """Return a valid password based on user input."""
    while True:
        mail_password1 = getpass(
            prompt=f"Type in your email password or hit ENTER to leave '{DEFAULT_PASSWORD}': "
        )
        mail_password2 = getpass(prompt="Type in your email password again: ")
        if mail_password1 == mail_password2:
            return mail_password1
        else:
            print("Your passwords don't match. Try again.")
            continue


def get_mail_server(mail_server: str = None, responses: Optional[Iterable[str]] = None):
    """Return a valid email address based on user input."""
    if responses is None:
        # An infinite stream of calls to input()
        responses = iter(
            lambda: input(
                f"Type in your email (eg. {DEFAULT_EMAIL_SERVER}) or hit ENTER to leave {DEFAULT_EMAIL_SERVER}): "
            ),
            None,
        )

    for mail_server in responses:
        if Validator().validate_server_address(mail_server):
            return mail_server
        elif mail_server == "":
            return DEFAULT_EMAIL_SERVER
        else:
            print(
                "Mail server should contain 3 groups of letters separated \
#                     by commas, eg. smtp.example.com"
            )
    else:
        # Note: cannot be raised from the default value of responses
        raise ValueError("Unexpected end of responses")


def get_db_secret_key(
    secret_key1: str = None,
    secret_key2: str = None,
    responses1: Optional[Iterable[str]] = None,
    responses2: Optional[Iterable[str]] = None,
):
    """Return a valid database secret key based on user input."""

    if responses1 is None:
        # An infinite stream of calls to input()
        responses1 = iter(
            lambda: getpass(
                f"Set your database secret key or hit ENTER to leave '{DEFAULT_PASSWORD}': "
            ),
            None,
        )
    if responses2 is None:
        # An infinite stream of calls to input()
        responses2 = iter(
            lambda: getpass("Type in your database secret key again: "),
            None,
        )
    for secret_key1 in responses1:
        for secret_key2 in responses2:
            if secret_key1 == secret_key2:
                if secret_key1 == "":
                    return DEFAULT_PASSWORD
                return secret_key2
            else:
                print("Your passwords don't match. Try again.")
                break

    else:
        # Note: cannot be raised from the default value of responses
        raise ValueError("Unexpected end of responses")


if __name__ == "__main__":
    update_credentials()
