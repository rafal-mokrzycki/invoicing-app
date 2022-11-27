#!/usr/bin/env python
"""
To run type: flask --app hello run
"""


import repackage

repackage.up(1)
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config_files.config import credentials, settings

CURRENCY = "PLN"
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.update(credentials)
mail = Mail(app)
db = SQLAlchemy(app)
Base = declarative_base()
engine = create_engine(
    "sqlite:///database.db",
    # connect_args={"port": 3306},
    # echo="debug",
    # echo_pool=True,
)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def format_percentages(number):
    """Formats a floating point number into string, i.e. 0.23 -> '23%'"""
    return str(int(number * 100)) + "%"


def format_number(number):
    """Formats a floating point number into string iwht a currency code, i.e. 2.50 -> '2.50 PLN'"""
    return "{:.2f}".format(number) + f" {CURRENCY}"


def get_number_of_objects_in_table(obejct):
    return db_session.query(obejct).count() + 1
