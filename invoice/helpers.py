#!/usr/bin/env python
"""
Helper functions
"""
import json
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import repackage

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from IPython.display import clear_output

repackage.up()
# from config_files.config import credentials

# app = Flask(__name__)
# app.config.update(credentials)

# db = SQLAlchemy(app)


def append_dict(dict1, dict2):
    """Appends one dictionary to another one keeping keys from both and returning
    a sum of their values as strings.
    """
    result = {}
    for i in set(list(dict1.keys()) + list(dict2.keys())):
        if i not in dict1:
            result[i] = dict2[i]
        elif i not in dict2:
            result[i] = dict1[i]
        else:
            result[i] = dict1[i] + dict2[i]
    for key in result:
        result[key] = str(result[key])
    return result


def get_currencies(filename="currencies.csv", columns=None, filepath=None):
    """Reads the CSV file with currency symbols and parses them to UI"""

    if columns is None:
        columns = ["Currency Code"]
    if filepath is None:
        filepath = repackage.add(f"../config_files/{filename}")
    df = pd.read_csv(filepath)
    df_selected = df[~df[columns].isin(["PLN", "EUR", "USD", "GBP", "JPY"])]
    if len(columns) == 1:
        return [
            ["PLN", "EUR", "USD", "GBP", "JPY"],
            df_selected[columns[0]].values.tolist(),
        ]
    else:
        return [
            ["PLN", "EUR", "USD", "GBP", "JPY"],
            df_selected[columns].values.tolist(),
        ]


def get_number_of_objects_in_table(database=None, table=None, object=None):
    query = f"""
    SELECT {object}, count({object})
    AS count FROM {table}
    GROUP BY {object};
    """
    list_of_tuples = [tuple(row) for row in database.execute(query).fetchall()]
    # invoices_counted_by_type = {}
    # for elem in list_of_tuples:
    #     print(elem[0])
    #     invoices_counted_by_type[elem[0]] = elem[1]
    return {elem[0]: elem[1] for elem in list_of_tuples}


def wait(step=1, max=3, string="Processing"):
    for x in range(0, max):
        display = string + "." * (x + 1)
        print(display, end="\r")
        time.sleep(step)
    clear_output(wait=True)


def send_email(
    sender_address,
    sender_pass,
    receiver_address,
    subject,
    body,
    filename=None,
    id=None,
):
    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    # The subject line
    message["Subject"] = subject
    # The body and the attachments for the mail
    message.attach(MIMEText(body, "plain"))

    if filename is not None and id is not None:
        if os.path.exists(
            f"{credentials['PATH_TO_DOWNLOAD_FOLDER']}/{filename}"
        ):
            os.remove()
        show_pdf(id=id, download=True)
        attach_file = open(filename, "rb")  # Open the file as binary mode
        # os search filename in downloads and remove
        payload = MIMEBase("application", "octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header(
            "Content-Decomposition", "attachment", filename=filename
        )
        message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP(
        credentials["MAIL_SERVER"], credentials["MAIL_PORT"]
    )
    # use gmail with port
    session.starttls()  # enable security
    session.login(
        sender_address, sender_pass
    )  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
