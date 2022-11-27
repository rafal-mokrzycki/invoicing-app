import csv

import pandas as pd

from app import Base, Contractor, User, db, db_session, engine


def populate_data():
    users = pd.read_csv("config_files/demo_accounts.csv")
    invoices = pd.read_csv("config_files/demo_invoices.csv")
    contractors = pd.read_csv("config_files/demo_contractors.csv")

    users.to_sql("accounts", con=engine, index=False, if_exists="replace")
    invoices.to_sql("invoices", con=engine, index=False, if_exists="replace")
    contractors.to_sql("contractors", con=engine, index=False, if_exists="replace")


populate_data()
