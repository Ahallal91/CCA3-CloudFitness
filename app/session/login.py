from flask import Blueprint, render_template

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
