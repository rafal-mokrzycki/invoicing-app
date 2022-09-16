#!/usr/bin/env python
from config_files.config import config
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(config)
# app.config["SECRET_KEY"] = "secret-key-goes-here"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = "accounts"
    email = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def get_id(self):
        return self.email


class Contractor(db.Model, UserMixin):
    __tablename__ = "contractors"
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    tax_no = db.Column(db.String(250), primary_key=True)

    def __repr__(self) -> str:
        return f"""
{self.name} {self.surname}
{self.tax_no}
"""


class Issuer(db.Model, UserMixin):
    __tablename__ = "issuers"
    name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    tax_no = db.Column(db.String(250), primary_key=True)
    bank_account = db.Column(db.String(250), nullable=False)

    def __init__(self) -> None:
        self.name = "Adam&Co."
        self.address = "Default address"
        self.tax_no = "123456789"
        self.bank_account = "00000000000000000000000000"

    def __repr__(self) -> str:
        return f"{self.name}\n\n{self.address}\n{self.tax_no}\nBank account: {self.bank_account}"
