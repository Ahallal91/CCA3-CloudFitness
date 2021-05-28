from flask import Blueprint, render_template

profile_bp = Blueprint(
    'profile_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@profile_bp.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html")