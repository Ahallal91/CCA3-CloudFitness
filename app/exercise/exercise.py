from flask import Blueprint, render_template
import app.dao.ExerciseDAO as ExerciseDAO


exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@exercise_bp.route('/exercise/<string:exercise_type>/<string:name>', methods=["GET", "POST"])
def exercise_page(exercise_type, name):
    exercise = ExerciseDAO.get_exercise(exercise_type, name)

    return render_template("exercise.html", exercise=exercise)
