from flask import Blueprint, render_template
import requests
from app.util import create_table_resource
from ..dao.ExerciseDAO import ExerciseDAO as ExerciseDAO

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

exerciseDAO = ExerciseDAO()

def getRandomQuote():
    response = requests.get('https://zenquotes.io/api/random')
    return response.json()[0]

@home_bp.route('/', methods=["GET", "POST"])
def home():
    quote = getRandomQuote()
    exercise = exerciseDAO.get_approved_exercises(None, None)
    print(exercise)
    return render_template("home.html", quote=quote, exercise=exercise)
