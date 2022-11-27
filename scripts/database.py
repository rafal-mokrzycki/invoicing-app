import pandas as pd
import repackage

repackage.up()
from app import Base, User, engine


def create_database(drop_all=True):
    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def populate_data():
    users = pd.read_csv("config_files/demo_accounts.csv")
    invoices = pd.read_csv("config_files/demo_invoices.csv")
    contractors = pd.read_csv("config_files/demo_contractors.csv")

    users.to_sql("accounts", con=engine, index=False, if_exists="replace")
    invoices.to_sql("invoices", con=engine, index=False, if_exists="replace")
    contractors.to_sql("contractors", con=engine, index=False, if_exists="replace")

    print("Database populated.")


def query():
    User.query.all()


if __name__ == "__main__":
    create_database()
    populate_data()
    print(query())
