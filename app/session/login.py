import requests, json
from flask import Blueprint, render_template, request, flash

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def verify_api(captcha):
    with open('app/config.json') as f:
                data = json.load(f)
    recaptcha_data = data.get('recaptcha-api')
    # verify with API
    result = requests.post(recaptcha_data['url'], data={
        'secret': recaptcha_data['secret-key'],
        'response': captcha,
        'remoteip': request.remote_addr,
    }).content
    result = json.loads(result)

    return result.get('success', None)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html") 
    if request.method =='POST':
        success = verify_api(request.form['g-recaptcha-response'])

        if success:
            flash('You have logged in')
            return render_template("login.html")
        else:
            flash('reCaptcha unsuccessful')
            return render_template("login.html")

