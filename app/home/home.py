from flask import Blueprint, render_template
import requests
import boto3

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def getRandomQuote():
    response = requests.get('https://zenquotes.io/api/random')
    return response.json()[0]

@home_bp.route('/', methods=["GET", "POST"])
def home():
    quote = getRandomQuote()
    return render_template("home.html", quote=quote)
