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


def get_exercise_image(id, imagetype):
    url = f"https://elasticbeanstalk-ap-southeast-2-059411200951.s3-ap-southeast-2.amazonaws.com/image_uploads/{id}.{imagetype}"
    return url


def getExercise():
    table = create_table_resource('exercise')
    response = table.scan()
    return response['Items']


@home_bp.route('/', methods=["GET", "POST"])
def home():
    #quote = getRandomQuote()
    quote = {'q': 'test quote', 'a': 'test author'}
    exercise = getExercise()
    for item in exercise:
        item['image_url'] = get_exercise_image(item['id'], item['filetype'])
    return render_template("home.html", quote=quote, exercise=exercise)
