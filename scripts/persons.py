#!/usr/bin/env python
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret-key-goes-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mybooks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "accounts"
    email = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def get_id(self):
        return self.email
