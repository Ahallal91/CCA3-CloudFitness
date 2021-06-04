from flask import Blueprint, render_template, request
from .management import Management as Management


pending_bp = Blueprint(
    'pending_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

management = Management()

@pending_bp.route('/pending', methods=["GET", "POST"])
def pending():
    exercises = management.get_exercise_by_approval('False')
    if request.method == 'GET':
        return render_template("pending.html", exercises=exercises)
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        approval = request.form['approval']
        if approval == 'approved':
            management.update_exercise_approval(type, name, True)

        return render_template("pending.html", exercises=exercises)

