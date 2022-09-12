"""
To run type: flask --app hello run
"""

import datetime
import re
import sqlite3

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from scripts.persons import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route("/")
def home():
    current_year = datetime.date.today().year
    return render_template("index.html", current_year=current_year)


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        # b_author = request.form["author"]
        # b_rating = request.form["rating"]
        new_user = User(
            email="asd@interia.pl",
            name=name,
            surname=name,
            phone_no="123-123-123",
            password="qweasd",
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")


def create_table(name="accounts"):
    cursor = sqlite3.connect("database.db", check_same_thread=False).cursor()
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {name} (
            email varchar(250) PRIMARY KEY,
            surname varchar(250) NOT NULL,
            name varchar(250) NOT NULL,
            phone_no varchar(250) NOT NULL,
            password varchar(250) NOT NULL)"""
    )


if __name__ == "__main__":
    app.run(debug=True)
