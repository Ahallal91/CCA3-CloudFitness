import requests, json
from flask import Blueprint, render_template, request, flash

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

secret_key = "6LdjNssaAAAAACf7R0kBGYlC1NqCHOaSpm44Pf_B"
recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method =='POST':
        # verify with API
        result = requests.post(recaptcha_url, data={
            'secret': secret_key,
            'response': request.form['g-recaptcha-response'],
            'remoteip': request.remote_addr,
        }).content
        result = json.loads(result)
        success = result.get('success', None)

        if success:
            flash('You have logged in')
            return render_template("login.html")
        else:
            flash('reCaptcha unsuccessful')
            return render_template("login.html")

