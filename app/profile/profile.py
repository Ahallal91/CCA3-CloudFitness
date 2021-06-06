from flask import Blueprint, render_template, session, url_for, flash, request
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
        if request.method == 'POST':
            exercise_type = request.form['type']
            exercise_name = request.form['name']
            if 'existing' in request.form:
                profileExistingDAO.remove_existing_exercise(exercise_type, exercise_name, session['email'])
            if 'personal' in request.form:
                profilePersonalDAO.remove_exercise(exercise_type, exercise_name, session['email'])
            flash('Removed Exercise from Profile')
        exercises = {}
        exercises['personal'] = profilePersonalDAO.get_exercises(session['email'])
        temp_existing_exercises = profileExistingDAO.get_existing_exercises(session['email'])
        exercises['existing'] = []
        for e in temp_existing_exercises:
            exercises['existing'] += exerciseDAO.get_exercise(e['exercise-type'], e['exercise-name'])
        
        return render_template("profile.html", exercises=exercises)
    
    flash("Please sign in before viewing your profile")
    return redirect(url_for('login_bp.login'))