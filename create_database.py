#!/usr/bin/env python
import json
from pathlib import Path

import repackage

repackage.up()
from config_files.config import load_config_file
from scripts.database import Database

# class Credentials:
#     def __init__(
#         self,
#         filepath,
#         secret_key,
#         mail_server,
#         mail_username,
#         mail_password,
#         path_to_download,
#     ):
#         self.filepath = filepath
#         self.secret_key = secret_key
#         self.mail_server = mail_server
#         self.mail_username = mail_username
#         self.mail_password = mail_password
#         self.path_to_download = path_to_download
#         self.database_filename = "database.db"
#         self.sqlalchemy_track_modifications = False
#         self.mail_use_tls = True
#         self.mail_use_ssl = False
#         self.mail_port = 587


def create_database():
    credentials = load_config_file(
        Path(__file__).parent.joinpath("config_files/credentials.json")
    )
    db = Database()
    db.create_table("invoices", drop_if_exists=True)
    db.create_table("accounts", drop_if_exists=True)
    db.create_table("contractors", drop_if_exists=True)


def update_credentials(
    filepath,
    secret_key,
    mail_server,
    mail_username,
    mail_password,
    path_to_download,
    database_filename="database.db",
    sqlalchemy_track_modifications=False,
    mail_use_tls=True,
    mail_use_ssl=False,
    mail_port=587,
):
    """Updates the credentials.json file"""
    json_path = "config_files/credentials.json"
    data = {}
    data["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}/{database_filename}"
    data["SECRET_KEY"] = secret_key
    data["SQLALCHEMY_TRACK_MODIFICATIONS"] = sqlalchemy_track_modifications
    data["MAIL_SERVER"] = mail_server
    data["MAIL_PORT"] = mail_port
    data["MAIL_USERNAME"] = mail_username
    data["MAIL_PASSWORD"] = mail_password
    data["MAIL_USE_TLS"] = mail_use_tls
    data["MAIL_USE_SSL"] = mail_use_ssl
    data["PATH_TO_DOWNLOAD_FOLDER"] = path_to_download
    with open(json_path, "w") as jsonFile:
        json.dump(data, jsonFile)


def feed_database():
    """Feeds database with sample data"""
    pass


if __name__ == "__main__":
    update_credentials(
        filepath="C:/Users/rafal/Documents/python/invoicing_app",
        secret_key="secret-key",
        mail_server="smtp.example.com",
        mail_username="example@example.com",
        mail_password="my-very-secret-password",
        path_to_download="some-folder",
    )
    create_database()
