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
from invoice.helpers import get_currencies, get_number_of_objects_in_table

bp = Blueprint("user", __name__)


@bp.route("/user")
@login_required
def user():
    return render_template("user/user.html")


@bp.route("/user/new_invoice", methods=("GET", "POST"))
@login_required
def new_invoice():
    invoice_number_on_type = get_number_of_objects_in_table(
        database=get_db(), table="invoice", object="invoice_type"
    )  # {"regular": 1, "proforma": 3, "advanced payment": 1}
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
                (invoice_type, invoice_no, issue_date, issue_city,
                issuer_tax_no, recipient_tax_no, item,amount, unit,
                price_net, tax_rate, sum_net, sum_gross, currency,
                sell_date, issuer_id)
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
        today=today.date(),
        min_date=(today - datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
        max_date=(today + datetime.timedelta(days=60)).strftime("%Y-%m-%d"),
        year_month=datetime.datetime.strftime(today, "%Y/%m/"),
    )


@bp.route("/user/your_invoices")
@login_required
def your_invoices():
    db = get_db()
    invoices = db.execute(
        "SELECT id, invoice_no, sum_net, sum_gross, recipient_tax_no, issue_date, sell_date, item"
        " FROM invoice"
        " ORDER BY issue_date DESC"
    ).fetchall()
    return render_template("user/your_invoices.html", invoices=invoices)


@bp.route("/user/your_invoices/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_invoice(id):
    """Method enables edition of existing invoices"""
    db = get_db()
    invoice = db.execute(f"SELECT * FROM invoice WHERE id = {id}").fetchone()
    if request.method == "POST":
        # invoice.id = invoice.id
        invoice_type = request.form.get("invoice_type")
        invoice_no = request.form.get("invoice_no")
        issue_date = request.form.get("issue_date")
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
        error = None
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
            UPDATE invoice
            SET invoice_type=?,
            invoice_no=?,
            issue_date=?,
            issue_city=?,
            issuer_tax_no=?,
            recipient_tax_no=?,
            item=?,
            amount=?,
            unit=?,
            price_net=?,
            tax_rate=?,
            sum_net=?,
            sum_gross=?
            WHERE id = ?""",
                (
                    invoice_no,
                    issue_date,
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
                    id,
                ),
            )
            db.commit()
        db.commit()
        return render_template("user/user.html")
    return render_template("user/edit_invoice.html", invoice=invoice)
    # db = get_db()
    # invoices = db.execute(
    #     "SELECT id, invoice_no, sum_net, sum_gross, recipient_tax_no, issue_date, sell_date, item"
    #     " FROM invoice"
    #     " ORDER BY issue_date DESC"
    # ).fetchall()
    # return render_template("user/your_invoices.html", invoices=invoices)
