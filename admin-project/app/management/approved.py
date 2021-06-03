from flask import Blueprint, render_template, request
from .management import Management as Management

approved_bp = Blueprint(
    'approved_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

management = Management()

@approved_bp.route('/approved', methods=["GET", "POST"])
def approved():
    exercises = management.get_exercise_by_approval(True)
    if request.method == 'GET':
        return render_template("approved.html", exercises=exercises)
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        pending = request.form['pending']
        if pending == 'pending':
            management.update_exercise_approval(type, name, False)
        return render_template("approved.html", exercises=exercises)