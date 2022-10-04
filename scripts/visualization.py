#!/usr/bin/env python
import calendar
import datetime
import json
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import pdfkit
import plotly
import plotly.express as px
import repackage
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

repackage.up()
from config_files.config import credentials, settings

from scripts.database import Contractor, User
from scripts.invoice import (
    InvoiceForm,
    format_number,
    format_percentages,
    get_number_of_invoices_in_db,
)
from scripts.parsers import parse_dict_with_invoices_counted

repackage.up()
from config_files.config import credentials, settings

from scripts.invoice import InvoiceForm

app = Flask(__name__)
app.config.update(credentials)

db = SQLAlchemy(app)


class DataHandler:
    def __init__(self, data=None, granularity=None) -> None:
        self.data = data

    def get_data(self):
        query = db.session.query(
            InvoiceForm.sum_gross, InvoiceForm.issue_date, InvoiceForm.invoice_type
        ).all()
        df = pd.DataFrame(query, columns=["SumGross", "IssueDate", "InvoiceType"])
        return df
