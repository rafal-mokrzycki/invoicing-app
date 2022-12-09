from flask import Blueprint, render_template

bp = Blueprint("index", __name__)


@bp.route("/")
@bp.route("/home")
def index():
    return render_template("index.html")
