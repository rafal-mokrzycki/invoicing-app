import sqlite3
import sys
import traceback

import repackage

repackage.up()
from config_files.config import config


class Database:
    def __init__(self, db_file=None) -> None:
        if db_file is None:
            self.db_file = config["DATABASE"]
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
        if table_name == "accounts":
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                email varchar(250) PRIMARY KEY,
                surname varchar(250) NOT NULL,
                name varchar(250) NOT NULL,
                phone_no varchar(250) NOT NULL,
                password varchar(250) NOT NULL)"""
        elif table_name == "contractors":
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                name varchar(250) NOT NULL,
                surname varchar(250) NOT NULL,
                tax_no varchar(250) PRIMARY KEY)"""
        elif table_name == "invoices":
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                invoice_type varchar(250) NOT NULL,
                invoice_no varchar(250) NOT NULL,
                issue_date DATE NOT NULL,
                issue_city varchar(250) NOT NULL,
                sell_date DATE NOT NULL,
                issuer_tax_no INTEGER NOT NULL,
                recipient_tax_no INTEGER  NOT NULL,
                position varchar(250) NOT NULL,
                amount REAL NOT NULL,
                unit varchar(250) NOT NULL,
                price_net REAL NOT NULL,
                tax_rate REAL NOT NULL,
                sum_net REAL NOT NULL,
                sum_gross REAL NOT NULL)"""
        elif table_name == "issuers":
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                name varchar(250) NOT NULL,
                address varchar(250) NOT NULL,
                bank_account varchar(250) NOT NULL,
                tax_no varchar(250) PRIMARY KEY)"""
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


if __name__ == "__main__":
    pass
    db = Database()
    db.create_table("invoices", drop_if_exists=True)
