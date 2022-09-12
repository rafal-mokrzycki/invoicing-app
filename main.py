"""
To run type: flask --app hello run
"""

import datetime
import re
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

APP = Flask(__name__)
CURSOR = sqlite3.connect("database.db", check_same_thread=False).cursor()


@APP.route("/")
def home():
    current_year = datetime.date.today().year
    return render_template("index.html", current_year=current_year)


# Route for handling the login page logic
@APP.route("/login", methods=["GET", "POST"])
def login():
    error = None
    return render_template("login.html", error=error)


@APP.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


def create_table(name="accounts"):
    CURSOR.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {name} (
            email varchar(250) PRIMARY KEY,
            surname varchar(250) NOT NULL,
            name varchar(250) NOT NULL,
            phone_no varchar(250) NOT NULL,
            password varchar(250) NOT NULL)"""
    )


if __name__ == "__main__":
    APP.run(debug=True)
