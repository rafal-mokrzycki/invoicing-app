#!/usr/bin/env python
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from invoice.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        plan = request.form["plan"]
        terms = request.form["terms"]
        newsletter = request.form["newsletter"]
        name = request.form["name"]
        surname = request.form["surname"]
        phone_no = request.form["phone_no"]
        db = get_db()
        error = None
        if not email:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        if error is None:
            try:
                db.execute(
                    """INSERT INTO user
                    (email, password, plan, terms, newsletter, name,
                    surname, phone_no)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        email,
                        generate_password_hash(
                            password, method="pbkdf2:sha256", salt_length=8
                        ),
                        plan,
                        terms,
                        newsletter,
                        name,
                        surname,
                        phone_no,
                    ),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE email = ?", (email,)
        ).fetchone()
        # Email doesn't exist or password incorrect.
        if user is None:
            error = "That email does not exist, please try again.."
        elif not check_password_hash(user["password"], password):
            error = "Password incorrect, please try again."
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error)
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute("SELECT * FROM user WHERE id = ?", (user_id,))
            .fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.route("/reset_password", methods=("GET", "POST"))
def reset_password():
    return render_template("auth/reset_password.html")


@bp.route("/checkout/<string:plan>")
def checkout(plan):
    return render_template("auth/checkout.html")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
