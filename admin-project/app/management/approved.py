from flask import Blueprint, render_template, request
from .management import Management as management

approved_bp = Blueprint(
    'approved_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@approved_bp.route('/approved', methods=["GET", "POST"])
def approved():
    exercises = management.get_exercise_by_approval(True)
    if request.method == 'GET':
        return render_template("approved.html", exercises=exercises)
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        approval = request.form['approval']
        management.update_exercise_approval(type, name, approval)
        return render_template("approved.html", exercises=exercises)