#!/usr/bin/env python
import sqlite3
import sys
import traceback

import repackage

repackage.up(1)
from config_files.config import credentials, settings
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

app = Flask(__name__)
app.config.update(credentials)

db = SQLAlchemy(app)

Base = declarative_base()


class Database:
    """
    A class used to represent a Database

    Attributes
    ----------
    db_file : str
        database file name, default=None, if not passed explicitly then database.db

    Methods
    -------
    create_table(table_name : str, conn : sqlite3.Connection=None, drop_if_exists=False)
        Creates a table of a given table_name.

    __drop_table__(table_name: str, conn: sqlite3.Connection = None)
        Drops a table of a given table_name.

    add_record(record_to_add: list,table_name: str,conn: sqlite3.Connection = None)
        Not yet implemented. Adds a record to a table of a given table_name.

    __delete_record__(id_record_to_delete: int, table_name: str, conn: sqlite3.Connection = None)
        Not yet implemented. Deletes a record from a table of a given table_name.
    """

    def __init__(self, db_file: str = None) -> None:
        if db_file is None:
            self.db_file = settings["DATABASE"]
        else:
            self.db_file = db_file

    def create_table(
        self, table_name: str, conn: sqlite3.Connection = None, drop_if_exists=False
    ):
        """Creates a table of a given table_name.

        Parameters
        ----------
        table_name : str
            one of "accounts", "contractors" or "invoices"
        conn : sqlite3.Connection, optional
            opens a connection to an SQLite database
        drop_if_exists : boolean, default=False
            if True drops an existing table of a given name

        Raises
        ------
        NameError
            If a wrong table_name is passed.
        """
        connection = conn or create_connection(self.db_file)
        # create table ACCOUNTS
        if table_name == settings["TABLE_NAMES"][0]:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY ASC,
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
                id INTEGER PRIMARY KEY ASC,
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
                id INTEGER PRIMARY KEY ASC,
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
                currency varchar(250) NOT NULL,
                issuer_id INTEGER NOT NULL,
                recipient_id INTEGER NOT NULL,
                FOREIGN KEY(recipient_id) REFERENCES contractors(id),
                FOREIGN KEY(issuer_id) REFERENCES accounts(id))"""
        else:
            raise NameError
        try:
            cursor = connection.cursor()
            if drop_if_exists:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            cursor.execute(create_table_sql)
            print(f"Table {table_name} created.")
        except sqlite3.Error as e:
            print("SQLite error: %s" % (" ".join(e.args)))
            print("Exception class is: ", e.__class__)
            print("SQLite traceback: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def __drop_table__(self, table_name: str, conn: sqlite3.Connection = None):
        """Drops a table of a given table_name.

        Parameters
        ----------
        table_name : str
            one of "accounts", "contractors" or "invoices"
        conn : sqlite3.Connection, optional
            opens a connection to an SQLite database

        Raises
        ------
        NameError
            If a wrong table_name is passed.
        """
        if table_name not in settings["TABLE_NAMES"]:
            raise NameError("Wrong table name.")
        else:
            connection = conn or create_connection(self.db_file)
            cursor = connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"Table {table_name} dropped.")

    def add_record(
        self,
        record_to_add: list,
        table_name: str,
        conn: sqlite3.Connection = None,
    ):
        """Not yet implemented. Adds a record to a table of a given table_name.

        Parameters
        ----------
        record_to_add : list
            list o items to add
        table_name : str
            one of "accounts", "contractors" or "invoices"
        conn : sqlite3.Connection, optional
            opens a connection to an SQLite database

        Returns
        ------
        None
        """
        pass

    def __delete_record__(
        self,
        id_record_to_delete: int,
        table_name: str,
        conn: sqlite3.Connection = None,
    ):
        """Not yet implemented. Deletes a record from a table of a given table_name.

        Parameters
        ----------
        id_record_to_delete : int
            id of a record to delete
        table_name : str
            one of "accounts", "contractors" or "invoices"
        conn : sqlite3.Connection, optional
            opens a connection to an SQLite database

        Returns
        ------
        None
        """
        pass


class Invoice(Model, UserMixin, Base):
    """
    A class used to represent an Invoice. Inherits from Model, UserMixin and Base.

    Attributes
    ----------
    __tablename__ : str
        default="invoices"

    id : int
        primary key

    amount : float
        amount of goods in an item

    invoice_no : str
        invoice number, set automatically

    invoice_type : str
        invoice type, one of the following: "regular", "advanced payment", "proforma"

    issue_city : str
        issue city

    issue_date : date
        issue date

    issuer_tax_no : int
        issuer tax number

    item : str
        item / position

    price_net : float
        price net of a good

    recipient_tax_no : int
        recipient tax number

    sell_date : date
        sell date

    sum_gross : float
        sum gross (sum of all goods in an item * tax rate)

    sum_net : float
        sum net (sum of all goods in an item)

    tax_rate : float
        tax rate for an item, one of the following: 0.00, 0.05, 0.08, 0.23

    unit : str
        unit of an item

    currency : str
        currency of an item

    issuer_id : int
        issuer id, foreign key

    recipient_id : int
        recipient id, foreign key
    """

    __tablename__ = settings["TABLE_NAMES"][2]
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    invoice_no = Column(String(250), nullable=False)
    invoice_type = Column(String(250), nullable=False)
    issue_city = Column(String(250), nullable=False)
    issue_date = Column(Date, nullable=False)
    issuer_tax_no = Column(Integer, nullable=False)
    item = Column(String(250), nullable=False)
    price_net = Column(Float, nullable=False)
    recipient_tax_no = Column(Integer, nullable=False)
    sell_date = Column(Date, nullable=False)
    sum_gross = Column(Float, nullable=False)
    sum_net = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False)
    unit = Column(String(250), nullable=False)
    currency = Column(String(250), nullable=False)
    issuer_id = Column(Integer, ForeignKey("accounts.id"))
    recipient_id = Column(Integer, ForeignKey("contractors.id"))


class User(Model, UserMixin, Base):
    __tablename__ = settings["TABLE_NAMES"][0]
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=False)
    phone_no = Column(Integer, nullable=False)
    password = Column(String(250), nullable=False)
    company_name = Column(String(250), nullable=True)
    street = Column(String(250), nullable=True)
    house_no = Column(String(250), nullable=True)
    flat_no = Column(String(250), nullable=True)
    zip_code = Column(String(250), nullable=True)
    city = Column(String(250), nullable=True)
    tax_no = Column(String(250), nullable=True)
    bank_account = Column(String(250), nullable=True)
    plan = Column(String(250), nullable=False)
    terms = Column(Boolean, nullable=False)
    newsletter = Column(Boolean, nullable=False)


class Contractor(Model, UserMixin, Base):
    __tablename__ = settings["TABLE_NAMES"][1]
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=True)
    name = Column(String(250), nullable=True)
    surname = Column(String(250), nullable=True)
    phone_no = Column(Integer, nullable=True)
    company_name = Column(String(250), nullable=True)
    street = Column(String(250), nullable=True)
    house_no = Column(String(250), nullable=True)
    flat_no = Column(String(250), nullable=True)
    zip_code = Column(String(250), nullable=True)
    city = Column(String(250), nullable=True)
    tax_no = Column(String(250), nullable=True)
    bank_account = Column(String(250), nullable=True)
    # invoice_id = Column(Integer, ForeignKey("invoice.id"))


def create_connection(db_file: str):
    """Creates a database connection to the SQLite database specified by db_files.
    Parameters
    ----------
    db_file : str
        database file name (ex. database.db)

    Returns
    ------
    connection : sqlite3.Connection
        opens a connection to an SQLite database
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print("SQLite error: %s" % (" ".join(e.args)))
        print("Exception class is: ", e.__class__)
        print("SQLite traceback: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    return connection


if __name__ == "__main__":
    db = Database()
    db.create_table("invoices", drop_if_exists=True)
    db.create_table("accounts", drop_if_exists=True)
    db.create_table("contractors", drop_if_exists=True)
