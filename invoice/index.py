import repackage
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

repackage.up()
from invoice.auth import login_required
from invoice.db import get_db

bp = Blueprint("index", __name__)


@bp.route("/")
@bp.route("/home")
def index():
    # db = get_db()
    # posts = db.execute(
    #     "SELECT p.id, title, body, created, author_id, username"
    #     " FROM post p JOIN user u ON p.author_id = u.id"
    #     " ORDER BY created DESC"
    # ).fetchall()
    return render_template("index.html")
