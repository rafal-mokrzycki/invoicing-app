import pandas as pd
import repackage
from werkzeug.security import generate_password_hash

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
    # hashed_password = generate_password_hash(users["password"].iloc[0])
    users["password"] = users["password"].apply(lambda x: generate_password_hash(x))
    users.to_sql("accounts", con=engine, index=False, if_exists="replace")
    invoices.to_sql("invoices", con=engine, index=False, if_exists="replace")
    contractors.to_sql("contractors", con=engine, index=False, if_exists="replace")

    print("Database populated.")


if __name__ == "__main__":
    create_database()
    populate_data()
