#!/usr/bin/env python
import sqlite3
import sys
import traceback

import repackage

repackage.up(1)
from config_files.config import credentials, settings
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

app = Flask(__name__)
app.config.update(credentials)

db = SQLAlchemy(app)

Base = declarative_base()


class Database:
    def __init__(self, db_file=None) -> None:
        if db_file is None:
            self.db_file = settings["DATABASE"]
        else:
            self.db_file = db_file

    def create_connection(self):
        """create a database connection to the SQLite database
            specified by db_files
        :param db_file: database file
        :return: Connection object or None
        """
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except sqlite3.Error as e:
            print("SQLite error: %s" % (" ".join(e.args)))
            print("Exception class is: ", e.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

        return connection

    def create_table(self, table_name, conn=None, drop_if_exists=False):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        connection = conn or self.create_connection()
        # create table ACCOUNTS
        if table_name == settings["TABLE_NAMES"][0]:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                email varchar(250) NOT NULL,
                surname varchar(250) NOT NULL,
                name varchar(250) NOT NULL,
                phone_no varchar(250) NOT NULL,
                password varchar(250) NOT NULL,
                tax_no varchar(250),
                bank_account varchar(250),
                company_name varchar(250),
                street varchar(250),
                house_no varchar(250),
                flat_no varchar(250),
                zip_code varchar(250),
                city varchar(250),
                plan varchar(250) NOT NULL,
                terms INTEGER NOT NULL,
                newsletter INTEGER NOT NULL
                )"""
        # create table CONTRACTORS
        elif table_name == settings["TABLE_NAMES"][1]:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                email varchar(250),
                surname varchar(250),
                name varchar(250),
                phone_no varchar(250),
                tax_no varchar(250),
                bank_account varchar(250),
                company_name varchar(250),
                street varchar(250),
                house_no varchar(250),
                flat_no varchar(250),
                zip_code varchar(250),
                city varchar(250))"""
        # create table INVOICES
        elif table_name == settings["TABLE_NAMES"][2]:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                amount REAL NOT NULL,
                invoice_no varchar(250) NOT NULL,
                invoice_type varchar(250) NOT NULL,
                issue_city varchar(250) NOT NULL,
                issue_date DATE NOT NULL,
                issuer_tax_no INTEGER NOT NULL,
                item varchar(250) NOT NULL,
                price_net REAL NOT NULL,
                recipient_tax_no INTEGER NOT NULL,
                sell_date DATE NOT NULL,
                sum_gross REAL NOT NULL,
                sum_net REAL NOT NULL,
                tax_rate REAL NOT NULL,
                unit varchar(250) NOT NULL,
                issuer_id REAL,
                recipient_id REAL,
                currency varchar(250) NOT NULL)"""
        else:
            raise NameError
        try:
            cursor = connection.cursor()
            if drop_if_exists:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print("SQLite error: %s" % (" ".join(e.args)))
            print("Exception class is: ", e.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def __drop_table__(self, table_name, conn=None):
        connection = conn or self.create_connection()
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    def add_record(self, db_file, table_name):
        pass

    def __delete_record__(self, db_file, table_name, key):
        pass


class Invoice(db.Model, UserMixin, Base):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    invoice_no = db.Column(db.String(250), nullable=False)
    invoice_type = db.Column(db.String(250), nullable=False)
    issue_city = db.Column(db.String(250), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    issuer_tax_no = db.Column(db.Integer, nullable=False)
    item = db.Column(db.String(250), nullable=False)
    price_net = db.Column(db.Float, nullable=False)
    recipient_tax_no = db.Column(db.Integer, nullable=False)
    sell_date = db.Column(db.Date, nullable=False)
    sum_gross = db.Column(db.Float, nullable=False)
    sum_net = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(250), nullable=False)
    currency = Column(db.String(250), nullable=False)
    issuer_id = Column(Integer, ForeignKey("accounts.id"))
    recipient_id = Column(Integer, ForeignKey("contractors.id"))

class User(db.Model, UserMixin, Base):
    __tablename__ = settings["TABLE_NAMES"][0]
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    company_name = db.Column(db.String(250), nullable=True)
    street = db.Column(db.String(250), nullable=True)
    house_no = db.Column(db.String(250), nullable=True)
    flat_no = db.Column(db.String(250), nullable=True)
    zip_code = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(250), nullable=True)
    tax_no = db.Column(db.String(250), nullable=True)
    bank_account = db.Column(db.String(250), nullable=True)
    plan = db.Column(db.String(250), nullable=False)
    terms = db.Column(db.Boolean, nullable=False)
    newsletter = db.Column(db.Boolean, nullable=False)


class Contractor(db.Model, UserMixin, Base):
    __tablename__ = settings["TABLE_NAMES"][1]
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    surname = db.Column(db.String(250), nullable=True)
    phone_no = db.Column(db.Integer, nullable=True)
    company_name = db.Column(db.String(250), nullable=True)
    street = db.Column(db.String(250), nullable=True)
    house_no = db.Column(db.String(250), nullable=True)
    flat_no = db.Column(db.String(250), nullable=True)
    zip_code = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(250), nullable=True)
    tax_no = db.Column(db.String(250), nullable=True)
    bank_account = db.Column(db.String(250), nullable=True)
    # invoice_id = db.Column(db.Integer, ForeignKey("invoice.id"))


if __name__ == "__main__":
    pass
    # db = Database()
    # db.create_table("invoices", drop_if_exists=True)
    # db.create_table("accounts", drop_if_exists=True)
    # db.create_table("contractors", drop_if_exists=True)
