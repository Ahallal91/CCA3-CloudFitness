from flask import Blueprint, render_template
import requests
from app.util import create_table_resource

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def getRandomQuote():
    response = requests.get('https://zenquotes.io/api/random')
    return response.json()[0]


def getExercise():
    table = create_table_resource('exercise')
    response = table.scan()
    return response['Items']


@home_bp.route('/', methods=["GET", "POST"])
def home():
    quote = getRandomQuote()
    exercise = getExercise()
    return render_template("home.html", quote=quote, exercise=exercise)
