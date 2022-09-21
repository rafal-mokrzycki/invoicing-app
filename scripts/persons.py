#!/usr/bin/env python
from config_files.config import config
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)
