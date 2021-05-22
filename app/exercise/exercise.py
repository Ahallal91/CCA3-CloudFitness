from boto3.dynamodb.conditions import Key
from app.util import create_table_resource
from flask import Blueprint, render_template, request, flash, session, redirect, url_for

exercise_bp = Blueprint(
    'exercise_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def getExercise(id):
    table = create_table_resource('exercise')
    response = table.query(
        KeyConditionExpression=Key('id').eq(id)
    )

    return response['Items']
    
@exercise_bp.route('/exercise/<id>', methods=["GET", "POST"])
def exercise(id):
    exercise = getExercise(id)
    return render_template("exercise.html", exercise=exercise)