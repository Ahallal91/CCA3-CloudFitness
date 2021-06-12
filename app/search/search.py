from flask import Blueprint, render_template, request, flash, redirect
from ..dao.ExerciseDAO import ExerciseDAO as ExerciseDAO

search_bp = Blueprint(
    'search_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

exerciseDAO = ExerciseDAO()

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get("query", None)

    list_of_exercises = exerciseDAO.search_by_query(query)

    for exercise in list_of_exercises:
        if not exercise["approved"]:
            list_of_exercises.remove(exercise)

    if not list_of_exercises:
        flash("No results")

    return render_template("search.html", list_of_exercises=list_of_exercises)
