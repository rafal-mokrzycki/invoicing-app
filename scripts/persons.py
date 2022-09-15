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
