"""to run: python -m create_database.py"""
#!/usr/bin/env python
import json
from pathlib import Path

import chardet
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config_files.config import settings
from scripts.validators import Validator

Base = declarative_base()
Valid = Validator()


def main():
    # create credentials.json file with default settings for a DB
    c = Credentials()
    c.mail_username, c.mail_password, c.mail_server, c.secret_key = get_required_info()
    c._change_default_credentials()
    c._update_credentials()

    # create a database (database.db file with all the required tables, yet empty)
    create_database()

    # feed tables with sample data
    feed_database()


class Credentials:
    """Creates a table of a given table_name.

    Parameters
    ----------
    _mail_username : str, default None
        mail username
    _mail_password : str, default None
        mail password
    _mail_server : str, default None
        mail server
    _secret_key : str, default None
        database secret key
    _download_folder : str, default 'path/to/your/user/Downloads'
        download folder
    _database_path : str, default 'path/to/your/repo/database.db'
        path o the database file
    __sqlalchemy_track_modifications : bool, default False
        if sqlalchemy should track modifications
    mail_use_tls : bool, default True
        if mail should use TLS
    mail_use_ssl : bool, default False
        if mail should use SSL
    mail_port : int, default 587
        mail port

    Methods
    ------
    print_default_credentials(choice)
    _change_default_credentials()
    _apply_changes()
    _update_credentials()
    """

    def __init__(self) -> None:
        self._mail_username: str = None
        self._mail_password: str = None
        self._mail_server: str = None
        self._secret_key: str = None
        self._download_folder: str = str(Path.home() / "Downloads")
        self._database_path: str = f"{Path(__file__).parent.resolve()}\database.db"
        self.__sqlalchemy_track_modifications: bool = False
        self.mail_use_tls: bool = True
        self.mail_use_ssl: bool = False
        self.mail_port: int = 587

    def print_default_credentials(self, choice=True):
        """Prints default credentials used for the credentials.json file.
        Sets Credentials class attributes."""
        if choice:
            numbers = [f"[{n+1}] " for n in list(range(9))] + ["(unchengable) "]
        else:
            numbers = [f"[{n+1}] " for n in list(range(10))]
        input_string = f"""
{numbers[0]} Mail address: {self.mail_username}
{numbers[1]} Mail password: {self.mail_password}
{numbers[2]} Mail server: {self.mail_server}
{numbers[3]} Download folder ('PATH_TO_DOWNLOAD_FOLDER'): '{self.download_folder}'
{numbers[4]} Database path ('SQLALCHEMY_DATABASE_URI'): '{self.database_path}'
{numbers[5]} Database secret key ('SECRET_KEY'): '{self.secret_key}'
{numbers[6]} 'MAIL_USE_TLS': {self.mail_use_tls}
{numbers[7]} 'MAIL_USE_SSL': {self.mail_use_ssl}
{numbers[8]} 'MAIL_PORT': {self.mail_port}
{numbers[9]} 'SQLALCHEMY_TRACK_MODIFICATIONS': {self.__sqlalchemy_track_modifications}
"""
        return input_string

    def _change_default_credentials(self):
        """Prints default credentials used for the credentials.json file
        and enables the user to change them. Sets Credentials class attributes."""
        print(
            f"""{'='*60}\nYour default credentials are as follows:
{self.print_default_credentials(choice=False)}"""
        )
        while True:
            change = input("Do you want to change any of these? [Y/n]\t")
            if change == "n":
                ("No changes applied.")
                break
            elif change == "Y":
                self._apply_changes()
                print("Changes applied.")
                break
            else:
                continue
        print("File credentials.json successfully created.")

    def _apply_changes(self):
        """Enables the user to change default credentials but selecting a number of
        a Credentials class attribute."""

        while True:
            number = input(
                f"""{'='*60}\nType in the number of parameter you want to change or [q] to quit:
{self.print_default_credentials(choice=True)}{'='*60}
"""
            )
            match number:
                case "1":
                    self.mail_username = get_and_check_email()
                case "2":
                    self.mail_password = get_and_check_password()
                case "3":
                    self.mail_server = get_mail_server()
                case "4":
                    self.download_folder = input(
                        f"Type in your download folder (current: {self.download_folder}): "
                    )
                case "5":
                    self.database_path = input(
                        f"Type in your database path (current: {self.database_path}): "
                    )
                case "6":
                    self.secret_key = get_db_secret_key()
                case "7":
                    self.mail_use_tls = Validator().is_boolean_input(
                        input(
                            f"Should your mail use TLS [T/F] (current: {self.mail_use_tls})? "
                        )
                    )
                case "8":
                    self.mail_use_ssl = Validator().is_boolean_input(
                        input(
                            f"Should your mail use SSL [T/F] (current: {self.mail_use_ssl})? "
                        )
                    )
                case "9":
                    self.mail_port = self.mail_port or Validator().validate_server_port(
                        Validator().is_integer_input(
                            input(
                                f"Type in your mail port (current: {self.mail_port}): "
                            )
                        )
                    )

                case _:
                    break

    def _update_credentials(self):
        """Takes Credentials class attributes and saves them to credentials.json."""
        json_path = "config_files/credentials_example.json"
        data = {}
        data["SQLALCHEMY_DATABASE_URI"] = self._database_path
        data["SECRET_KEY"] = self.secret_key
        data["SQLALCHEMY_TRACK_MODIFICATIONS"] = self.__sqlalchemy_track_modifications
        data["MAIL_SERVER"] = self._mail_server
        data["MAIL_PORT"] = self.mail_port
        data["MAIL_USERNAME"] = self._mail_username
        data["MAIL_PASSWORD"] = self._mail_password
        data["MAIL_USE_TLS"] = self.mail_use_tls
        data["MAIL_USE_SSL"] = self.mail_use_ssl
        data["PATH_TO_DOWNLOAD_FOLDER"] = self._download_folder
        with open(json_path, "w") as jsonFile:
            json.dump(data, jsonFile)

    @property
    def mail_username(self):
        return self._mail_username

    @mail_username.setter
    def mail_username(self, value):
        self._mail_username = value

    @property
    def mail_password(self):
        return self._mail_password

    @mail_password.setter
    def mail_password(self, value):
        self._mail_password = value

    @property
    def mail_server(self):
        return self._mail_server

    @mail_server.setter
    def mail_server(self, value):
        self._mail_server = value

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    @property
    def download_folder(self):
        return self._download_folder

    @download_folder.setter
    def download_folder(self, value):
        self._download_folder = value

    @property
    def database_path(self):
        return self._database_path

    @database_path.setter
    def database_path(self, value):
        self._database_path = value


def create_database():
    """Initializes Database class instance and creates required tables."""
    from scripts.database import Database

    db = Database()
    db.create_table("invoices", drop_if_exists=True)
    db.create_table("accounts", drop_if_exists=True)
    db.create_table("contractors", drop_if_exists=True)


def get_required_info():
    """Returns user email, password, mail server and database secret key."""
    return (
        get_and_check_email(),
        get_and_check_password(),
        get_mail_server(),
        get_db_secret_key(),
    )


def get_and_check_email():
    """Returns a valid email address based on user input."""
    while True:
        mail_username = input("Type in your email (or [q] to quit): ")
        if Validator().validate_email_address(mail_username):
            return mail_username
        elif mail_username == "q" or mail_username == "Q":
            return
        else:
            print("Wrong email format. Try again.")
            continue


def get_and_check_password():
    """Returns a valid password based on user input."""
    while True:
        mail_password1 = input("Type in your email password (or [q] to quit): ")
        if mail_password1 == "q" or mail_password1 == "Q":
            break
        mail_password2 = input("Type in your email password again (or [q] to quit): ")
        if mail_password2 == "q" or mail_password2 == "Q":
            break
        elif mail_password1 == mail_password2:
            return mail_password1
        else:
            print("Your passwords don't match. Try again.")
            continue


def get_mail_server():
    """Returns a valid mail server based on user input."""
    while True:
        mail_server = input(
            "Type in your mail server (eg. smtp.example.com or [q] to quit): "
        )
        if mail_server == "q" or mail_server == "Q":
            return
        elif Validator().validate_server_address(mail_server):
            return mail_server
        else:
            print(
                "Mail server should contain 3 groups of letters separated \
                    by commas, eg. smtp.example.com"
            )
            continue


def get_db_secret_key():
    """Returns a valid database secret key based on user input."""
    while True:
        secret_key1 = input("Set your database secret key (or [q] to quit): ")
        if secret_key1 == "q" or secret_key1 == "Q":
            return
        secret_key2 = input("Type in your database secret key again (or [q] to quit): ")
        if secret_key2 == "q" or secret_key2 == "Q":
            return
        elif secret_key1 == secret_key2:
            return secret_key2
        else:
            print("Your passwords don't match. Try again.")
            continue


def feed_database():
    """Reads CSV files and inserts the data to dataset's tables."""
    from config_files.config import credentials

    engine = create_engine(credentials["SQLALCHEMY_DATABASE_URI"])
    for table_name in settings["TABLE_NAMES"]:
        filepath = (
            f"{Path(__file__).parent.resolve()}\config_files\demo_{table_name}.csv"
        )
        with open(filepath, "rb") as f:
            result = chardet.detect(f.read())
            df = pd.read_csv(filepath, encoding=result["encoding"])
            df.to_sql(table_name, con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    main()
