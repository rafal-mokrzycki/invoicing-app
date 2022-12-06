#!/usr/bin/env python
"""
Database creation
"""
import argparse
import os
import time

import pandas as pd
import repackage
from credentials import update_credentials
from werkzeug.security import generate_password_hash

repackage.up()
from scripts.helpers import wait

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


def main():
    print("First you need to initialize credentials.json file.\n")
    time.sleep(1)
    update_credentials()
    wait(string="Database being initialized")
    create_database()
    if config["feed"].upper() == "YES":
        wait(string="Database being updated")
        feed_database()
    else:
        print("Database not fed with data.")


def create_database(drop_all=config["drop"]):
    from setup import Base, engine

    if drop_all.upper() == "YES":
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def feed_database():
    from setup import engine

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
    main()
