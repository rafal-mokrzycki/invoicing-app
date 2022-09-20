import calendar
import datetime

import repackage
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

repackage.up()
from config_files.config import config
from scripts.invoice import Invoice

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)


def parse_invoice_number(invoice_type):
    """
    Takes invoice type andbased on the current year and month, number of invoices in DB
    and pattern YYYY/MM/number_of_invoice parses invoice number.
    """
    currentDate = datetime.date.today()
    last_day_of_previous_month = datetime.date(
        currentDate.year,
        currentDate.month - 1,
        calendar.monthrange(currentDate.year, currentDate.month - 1)[1],
    )
    first_day_of_next_month = datetime.date(
        currentDate.year,
        currentDate.month + 1,
        1,
    )
    current_year = datetime.datetime.now().strftime("%Y")
    current_month = datetime.datetime.now().strftime("%m")
    query = (
        db.session.query(Invoice.invoice_type, func.count(Invoice.invoice_type))
        .group_by(Invoice.invoice_type)
        .filter(Invoice.issue_date > last_day_of_previous_month)
        .filter(Invoice.issue_date < first_day_of_next_month)
        .all()
    )
    try:
        invoice_number = [elem[1] for elem in query if elem[0] == invoice_type][0]
    except IndexError:
        invoice_number = 1
    return f"{current_year}/{current_month}/{invoice_number + 1}"


def func():
    return "YEY"


if __name__ == "__main__":
    # parse_invoice_number(invoice_type=None)
    func()

#########################################################################################
