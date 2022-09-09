"""
To run type: flask --app hello run
"""

import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
