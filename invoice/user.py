import repackage
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

repackage.up()
from invoice.auth import login_required
from invoice.db import get_db

bp = Blueprint("user", __name__)


@bp.route("/user")
def user():
    # db = get_db()
    # posts = db.execute(
    #     "SELECT p.id, title, body, created, author_id, username"
    #     " FROM post p JOIN user u ON p.author_id = u.id"
    #     " ORDER BY created DESC"
    # ).fetchall()
    return render_template("user/user.html")


@bp.route("/user/new_invoice", methods=("GET", "POST"))
def new_invoice():
    invoice_number_on_type = {"regular": 1, "proforma": 3, "advanced payment": 1}
    currencies = [["PLN", "USD", "GBP"]]
    return render_template(
        "user/new_invoice.html",
        invoice_number_on_type=invoice_number_on_type,
        currencies=currencies,
    )
