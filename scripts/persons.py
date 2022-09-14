#!/usr/bin/env python
from curses import get_tabsize

from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret-key-goes-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mybooks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "accounts"
    email = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def get_id(self):
        return self.email

    def get_token(self, expires_sec=300):
        serial = TimedJSONWebSignatureSerializer(
            app.config["SECRET_KEY"], expires_in=expires_sec
        )
        return serial.dumps({"email": self.email}).decode("utf-8")

    @staticmethod
    def verify_token(token):
        serial = TimedJSONWebSignatureSerializer(app.config["SECRET_KEY"])
        try:
            user_email = serial.loads(token)
        except:
            None
        return User.query.get(user_email)


class Contractor(db.Model, UserMixin):
    __tablename__ = "contractors"
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    tax_no = db.Column(db.String(250), nullable=False)

    def __repr__(self) -> str:
        return f"""
{self.name} {self.surname}
{self.tax_no}
"""
