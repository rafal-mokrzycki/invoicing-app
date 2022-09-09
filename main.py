"""
To run type: flask --app hello run
"""

import datetime
import re

import MySQLdb.cursors
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)


@app.route("/")
def home():
    current_year = datetime.date.today().year
    return render_template("index.html", current_year=current_year)


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = % s", (username,))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not email:
            msg = "Please fill out the form!"
        else:
            cursor.execute(
                "INSERT INTO accounts VALUES (NULL, % s, % s, % s)",
                (
                    username,
                    password,
                    email,
                ),
            )
            mysql.connection.commit()
            msg = "You have successfully registered !"
    elif request.method == "POST":
        msg = "Please fill out the form !"
    return render_template("register.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
