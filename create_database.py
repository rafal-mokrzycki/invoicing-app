#!/usr/bin/env python
import re
import time
from pathlib import Path


def main():
    mail = get_and_check_email()
    password = get_and_check_password()
    mail_server = get_mail_server()
    secret_key = get_db_secret_key()
    print_default_credentials()
    return mail, password, mail_server, secret_key


def get_and_check_email():
    while True:
        email = input("Type in your email (or [q] to quit): ")
        if (
            re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email)
            is not None
        ):
            return email
        elif email == ("q" or "Q"):
            break
        else:
            print("Wrong email format. Try again.")
            continue


def get_and_check_password():
    while True:
        password1 = input("Type in your email password (or [q] to quit): ")
        if password1 == ("q" or "Q"):
            break
        password2 = input("Type in your email password again (or [q] to quit): ")
        if password2 == ("q" or "Q"):
            break
        elif password1 == password2:
            return password1
        else:
            print("Your passwords don't match. Try again.")
            continue


def get_mail_server():
    while True:
        mail_server = input(
            "Type in your mail server (eg. smtp.example.com or [q] to quit): "
        )
        if mail_server == ("q" or "Q"):
            break
        else:
            return mail_server


def get_db_secret_key():
    while True:
        secret_key1 = input("Set your database secret key (or [q] to quit): ")
        if secret_key1 == ("q" or "Q"):
            break
        secret_key2 = input("Type in your database secret key again (or [q] to quit): ")
        if secret_key2 == ("q" or "Q"):
            break
        elif secret_key1 == secret_key2:
            return secret_key2
        else:
            print("Your passwords don't match. Try again.")
            continue


def print_default_credentials():
    download_folder = str(Path.home() / "Downloads")
    database_path = f"{Path(__file__).parent.resolve()}\database.db"
    print(
        f"""Your default credentials are as follows:
    Download folder ('PATH_TO_DOWNLOAD_FOLDER'): '{download_folder}'
    Database path ('SQLALCHEMY_DATABASE_URI'): '{database_path}'
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
    'MAIL_USE_TLS': True
    'MAIL_USE_SSL': False
    'MAIL_PORT': 587
"""
    )
    while True:
        change = input("Do you want to change any of these? [Y/n]\t")
        if change == "n":
            break
        elif change == "Y":
            make_changes()
            break
        else:
            continue


def make_changes():
    pass


def update_credentials(email):
    print(f"Your email is: {email}")


def create_database():
    print("create_database")


def feed_database():
    print("feed_database")


if __name__ == "__main__":
    # create credentials.json file with default settings for a DB
    # update_credentials()

    # create a database (database.db file with all the required tables, yet empty)
    # create_database()

    # feed tables with sample data
    # feed_database()

    # final ver
    # print(len(sys.argv))
    print_default_credentials()
    # update_credentials()
