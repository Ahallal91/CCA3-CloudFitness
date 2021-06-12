from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from ..dao.ExerciseDAO import ExerciseDAO as ExerciseDAO
from ..dao.CommentDAO import CommentDAO as CommentDAO
from ..dao.ProfileExistingDAO import ProfileExistingDAO as ProfileExistingDAO
from ..dao.ProfilePersonalDAO import ProfilePersonalDAO as ProfilePersonalDAO

exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

exerciseDAO = ExerciseDAO()
commentDAO = CommentDAO()
profileExistingDAO = ProfileExistingDAO()
profilePersonalDAO = ProfilePersonalDAO()

@exercise_bp.route('/exercise/<string:exercise_type>/<string:name>', defaults={'add': None}, methods=["GET", "POST"])
@exercise_bp.route('/exercise/<string:add>/<string:exercise_type>/<string:name>', methods=["GET", "POST"])
def exercise_page(exercise_type, name, add):
    exercise = exerciseDAO.get_exercise(exercise_type, name)
    if len(exercise) != 0:
        exercise = exercise[0]
    # update view count
    if add is None:
        exerciseDAO.update_exercise(exercise_type, name, "view", None)
    if add is not None and 'email' in session:
        profileExistingDAO.add_existing_exercise(exercise_type, name, session['email'])
    # post comment
    if request.method =='POST' and "message" in request.form:
        comment = request.form['message']
        if (len(comment) != 0 and 'email' in session):
            commentDAO.upload_comment(exercise_type, name, session['email'], comment)
        else:
            flash('Please login to post a comment')
            return redirect(url_for('login_bp.login'))
    # post like
    if request.method == 'POST' and "like" in request.form:
        like = request.form['like']
        if like is not None:
            exerciseDAO.update_exercise(exercise_type, name, None, "like")
            
    comments = commentDAO.get_comments(exercise_type, name)
    return render_template("exercise.html", exercise=exercise, comments=comments)

@exercise_bp.route('/personal/<string:exercise_type>/<string:name>', methods=["GET"])
def personal_exercise(exercise_type, name):
    if 'email' in session:
        exercises = profilePersonalDAO.get_exercise(exercise_type, name, session['email'])
        if len(exercises) != 0:
            exercises = exercises[0]

        return render_template("personal.html", exercises=exercises)

    flash("Please sign in before viewing your profile")
    return redirect(url_for('login_bp.login'))