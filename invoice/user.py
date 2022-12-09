import time

import pdfkit
import repackage
from flask import (
    Blueprint,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import abort

from config_files.config import credentials

repackage.up()
import datetime

from invoice.auth import login_required
from invoice.db import get_db
from invoice.formatters import format_number, format_percentages
from invoice.helpers import (
    get_currencies,
    get_number_of_objects_in_table,
    send_email,
)

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
        """SELECT id, invoice_no, sum_net, sum_gross, recipient_tax_no,
        issue_date, sell_date, item
         FROM invoice
         ORDER BY issue_date DESC"""
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
            sell_date=?,
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
                    invoice_type,
                    invoice_no,
                    issue_date,
                    issue_city,
                    sell_date,
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
        return render_template("user/user.html")
    return render_template("user/edit_invoice.html", invoice=invoice)


@bp.route("/user/your_invoices/show/<int:id>", methods=["GET", "POST"])
@login_required
def show_pdf(id, download=True):
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    db = get_db()
    invoice = db.execute(f"SELECT * FROM invoice WHERE id = {id}").fetchone()
    rendered = render_template(
        "user/pdf_template.html",
        amount=invoice["amount"],
        invoice_no=invoice["invoice_no"],
        invoice_type=invoice["invoice_type"].upper(),
        issue_city=invoice["issue_city"],
        issue_date=invoice["issue_date"],
        issuer_tax_no=invoice["issuer_tax_no"],
        item=invoice["item"],
        price_net=format_number(invoice["price_net"]),
        recipient_tax_no=invoice["recipient_tax_no"],
        sell_date=invoice["sell_date"],
        sum_gross=format_number(invoice["sum_gross"]),
        sum_net=format_number(invoice["sum_net"]),
        tax_string=format_percentages(invoice["tax_rate"]),
        unit=invoice["unit"],
    )
    pdf = pdfkit.from_string(rendered, False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    if download:
        response.headers[
            "Content-Disposition"
        ] = f"attachment; filename=Invoice_no_{invoice['invoice_no']}.pdf"
    else:
        response.headers[
            "Content-Disposition"
        ] = f"inline; filename=Invoice_no_{invoice['invoice_no']}.pdf"
    return response


@bp.route("/user/user_data", methods=["GET", "POST"])
@login_required
def user_data():
    db = get_db()
    user = db.execute(
        f"SELECT * FROM user WHERE id = {g.user['id']}"
    ).fetchone()
    if request.method == "POST":
        return redirect(url_for("user.user_data_edit"))
    return render_template("user/user_data.html", user=user)


@bp.route("/user/user_data_edit", methods=["GET", "POST"])
@login_required
def user_data_edit():
    db = get_db()
    user = db.execute(
        f"SELECT * FROM user WHERE id = {g.user['id']}"
    ).fetchone()
    if request.method == "POST":
        user_id = user["id"]
        # user.email = user['email']
        name = user["name"]
        surname = user["surname"]
        phone_no = request.form["phone_no"]
        company_name = request.form["company_name"]
        street = request.form["street"]
        house_no = request.form["house_no"]
        flat_no = request.form["flat_no"]
        zip_code = request.form["zip_code"]
        city = request.form["city"]
        tax_no = request.form["tax_no"]
        bank_account = request.form["bank_account"]
        error = None
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
            UPDATE user
            SET phone_no=?,
            name=?,
            surname=?,
            company_name=?,
            street=?,
            house_no=?,
            flat_no=?,
            zip_code=?,
            city=?,
            tax_no=?,
            bank_account=?
            WHERE id = ?""",
                (
                    phone_no,
                    name,
                    surname,
                    company_name,
                    street,
                    house_no,
                    flat_no,
                    zip_code,
                    city,
                    tax_no,
                    bank_account,
                    user_id,
                ),
            )
            db.commit()
        return redirect(url_for("user.user_data"))
    return render_template("user/user_data_edit.html", user=user, is_edit=True)


@bp.route("/user/your_invoices/send_email/<int:id>", methods=["GET", "POST"])
@login_required
def send_invoice_as_attachment(id):
    db = get_db()
    invoice = db.execute(f"SELECT * FROM invoice WHERE id = {id}").fetchone()
    user = db.execute(
        f"SELECT * FROM user WHERE id = {g.user['id']}"
    ).fetchone()
    recipient = "recipient@fake.com"  # Contractor.query.filter(invoice.recipient_id == Contractor.id).first()
    if request.method == "POST":
        send_email(
            id=invoice["id"],
            sender_address=request.form.get("issuer_email") or user["email"],
            sender_pass=credentials["MAIL_PASSWORD"],
            receiver_address=request.form.get("recipient_email"),
            subject=request.form.get("subject"),
            body=request.form.get("email_body"),
            filename=f"{credentials['PATH_TO_DOWNLOAD_FOLDER']}/Invoice_no_{invoice['invoice_no']}.pdf",
        )
        return render_template("user/your_invoices.html")
    return render_template(
        "user/send_email.html",
        invoice=invoice,
        user=user,
        recipient=recipient,
    )
    #     return render_template("user/user.html")
    # return render_template("user/edit_invoice.html", invoice=invoice)
