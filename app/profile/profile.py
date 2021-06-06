from flask import Blueprint, render_template, session, url_for, flash
from werkzeug.utils import redirect
from ..dao.ExerciseDAO import ExerciseDAO as ExerciseDAO
from ..dao.ProfileExistingDAO import ProfileExistingDAO as ProfileExistingDAO
from ..dao.ProfilePersonalDAO import ProfilePersonalDAO as ProfilePersonalDAO

profile_bp = Blueprint(
    'profile_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

profilePersonalDAO = ProfilePersonalDAO()
profileExistingDAO = ProfileExistingDAO()
exerciseDAO = ExerciseDAO()

@profile_bp.route('/profile', methods=["GET", "POST"])
def profile():
    if 'email' in session:
        exercises = profilePersonalDAO.get_exercises(session['email'])
        temp_existing_exercises = profileExistingDAO.get_existing_exercises(session['email'])
        for e in temp_existing_exercises:
            exercises.append(exerciseDAO.get_exercise(e['exercise-type'], e['exercise-name']))

        return render_template("profile.html", exercises=exercises)
    
    flash("Please sign in before viewing your profile")
    return redirect(url_for('login_bp.login'))