#!/usr/bin/env python
"""
Database creation
"""
import argparse
import os

import pandas as pd
import repackage
from werkzeug.security import generate_password_hash

repackage.up()
from app import Base, engine

parser = argparse.ArgumentParser(
    description="Initialization of a database with an option to feed it with sample data",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--drop",
    default="yes",
    choices=["yes", "no"],
    help="drop all exisiting tables and create new ones",
)
parser.add_argument(
    "--feed",
    default="yes",
    choices=["yes", "no"],
    help="feed database with sample data",
)
args = parser.parse_args()
config = vars(args)


def create_database(drop_all=config["drop"]):
    if drop_all.upper() == "YES":
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def feed_database():
    users = pd.read_csv(
        os.path.join(
            os.path.abspath(os.getcwd()),
            "config_files",
            "demo_accounts.csv",
        )
    )
    invoices = pd.read_csv(
        os.path.join(
            os.path.abspath(os.getcwd()),
            "config_files",
            "demo_invoices.csv",
        )
    )
    contractors = pd.read_csv(
        os.path.join(
            os.path.abspath(os.getcwd()),
            "config_files",
            "demo_contractors.csv",
        )
    )
    users["password"] = users["password"].apply(lambda x: generate_password_hash(x))

    users.to_sql("accounts", con=engine, index=False, if_exists="replace")
    invoices.to_sql("invoices", con=engine, index=False, if_exists="replace")
    contractors.to_sql("contractors", con=engine, index=False, if_exists="replace")
    print("Database fed with data.")


if __name__ == "__main__":
    create_database()
    if config["feed"].upper() == "YES":
        feed_database()
