from flask import Blueprint, render_template, request, session
import app.dao.ExerciseDAO as ExerciseDAO
from ..dao.CommentDAO import CommentDAO as CommentDAO

exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

commentDAO = CommentDAO()

@exercise_bp.route('/exercise/<string:exercise_type>/<string:name>', methods=["GET", "POST"])
def exercise_page(exercise_type, name):
    exercise = ExerciseDAO.get_exercise(exercise_type, name)
    # update view count
    ExerciseDAO.update_exercise(exercise_type, name, "view", None)
    if len(exercise) != 0:
        exercise = exercise[0]
    # post comment
    if request.method =='POST' and "message" in request.form:
        comment = request.form['message']
        if comment is not None:
            commentDAO.upload_comment(exercise_type, session['email'], comment)
    # post like
    if request.method == 'POST' and "like" in request.form:
        like = request.form['like']
        if like is not None:
            ExerciseDAO.update_exercise(exercise_type, name, None, "like")

    comments = commentDAO.get_comments(exercise_type)
    return render_template("exercise.html", exercise=exercise, comments=comments)
