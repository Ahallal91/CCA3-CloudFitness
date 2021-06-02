from flask import Blueprint, render_template
import requests


home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=["GET", "POST"])
def home():

    return render_template("home.html")
