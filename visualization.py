#!/usr/bin/env python
import json

import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, render_template


import datetime
import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pdfkit
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from config_files.config import credentials, settings
from scripts.database import Contractor, User
from scripts.invoice import (
    InvoiceForm,
    format_number,
    format_percentages,
    get_number_of_invoices_in_db,
)
from scripts.parsers import parse_dict_with_invoices_counted

app = Flask(__name__)


class DataHandler:
    pass
