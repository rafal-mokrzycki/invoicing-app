import time

import repackage
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import abort

repackage.up()
import datetime

from invoice.auth import login_required
from invoice.db import get_db
from invoice.helpers import get_currencies

bp = Blueprint("user", __name__)


@bp.route("/user")
def user():
    return render_template("user/user.html")


@login_required
@bp.route("/user/new_invoice", methods=("GET", "POST"))
def new_invoice():
    invoice_number_on_type = {"regular": 1, "proforma": 3, "advanced payment": 1}
    currencies = get_currencies()
    today = datetime.datetime.now()
    if request.method == "POST":
        # id=get_number_of_objects_in_table(Invoice)
        invoice_type = request.form.get("invoice_type")
        invoice_no = request.form.get("invoice_no")
        issue_date = today.date()
        issue_city = request.form.get("issue_city")
        sell_date = datetime.datetime.strptime(
            request.form.get("sell_date"), "%Y-%m-%d"
        ).date()
        issuer_tax_no = request.form.get("issuer_tax_no")
        recipient_tax_no = request.form.get("recipient_tax_no")
        item = request.form.get("item")
        amount = request.form.get("amount")
        unit = request.form.get("unit")
        price_net = request.form.get("price_net")
        tax_rate = request.form.get("tax_rate")
        sum_net = request.form.get("sum_net")
        sum_gross = request.form.get("sum_gross")
        currency = request.form.get("currency")
        issuer_id = 1  # TODO: fix for the currently logged in user
        error = None
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """INSERT INTO invoice
                (invoice_type, invoice_no, issue_date, issue_city, issuer_tax_no,
                recipient_tax_no, item,amount, unit, price_net, tax_rate, sum_net,
                sum_gross, currency, sell_date, issuer_id)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    invoice_type,
                    invoice_no,
                    issue_date,
                    issue_city,
                    issuer_tax_no,
                    recipient_tax_no,
                    item,
                    amount,
                    unit,
                    price_net,
                    tax_rate,
                    sum_net,
                    sum_gross,
                    currency,
                    sell_date,
                    issuer_id,
                ),
            )
            db.commit()
            return render_template("user/user.html")

    return render_template(
        "user/new_invoice.html",
        invoice_number_on_type=invoice_number_on_type,
        currencies=currencies,
    )
