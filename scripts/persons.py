from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mybooks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "accounts"
    email = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
