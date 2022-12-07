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
        db = get_db()
        error = None

        if not email:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    """INSERT INTO user (email, password, plan, terms, newsletter)
                    VALUES (?, ?, ?, ?, ?)""",
                    (
                        email,
                        generate_password_hash(
                            password, method="pbkdf2:sha256", salt_length=8
                        ),
                        plan,
                        terms,
                        newsletter,
                    ),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")
