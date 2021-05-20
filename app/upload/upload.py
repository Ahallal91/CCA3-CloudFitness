from flask import Blueprint, render_template

upload_bp = Blueprint(
    'upload_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@upload_bp.route('/upload', methods=["GET", "POST"])
def upload():
    return render_template("upload.html")