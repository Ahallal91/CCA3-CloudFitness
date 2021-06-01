import requests
import json
import uuid
import boto3
import bcrypt
from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from .register import register_user

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

encoding = 'utf-8'

with open('app/data.json') as f:
    data = json.load(f)
   
def get_login(email):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('user')
    response = table.get_item(Key={'email': email})

    if 'Item' in response:
        return response['Item']
    else:
        return None

def verify_captcha_api(captcha):
    recaptcha_data = data.get('recaptcha-api')
    # verify with API
    result = requests.post(recaptcha_data['url'], data={
        'secret': recaptcha_data['secret-key'],
        'response': captcha,
        'remoteip': request.remote_addr,
    }).content
    result = json.loads(result)

    return result.get('success', None)

def validate_captcha(captcha):
    success = verify_captcha_api(captcha)
    if success:
        return None
    else:
        return 'reCaptcha unsuccessful'

def validate_password(password, email):
    if email is not None:
        if bcrypt.checkpw(password, email['password'].encode(encoding)):
            return None
    return 'Username or password incorrect'

def set_session_id(email):
    session['email'] = email

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    session.pop('_flashes', None)
    if request.method == 'GET':    
        return render_template("login.html") 
    if request.method =='POST':
        error = False
        captcha = validate_captcha(request.form['g-recaptcha-response'])
        email = get_login(request.form['email'])
        password = request.form['password'].encode(encoding)
        password_valid = validate_password(password, email)

        if captcha is not None:
            flash(captcha)
            error = True
        if password_valid is not None:
            flash(password_valid)
            error = True
        if error:
            return render_template("login.html")
        else:
            flash('Successfully logged in')
            set_session_id(email)
            return redirect(url_for('home_bp.home'))

@login_bp.route("/facebook_login", methods=["POST"])
def facebook_login():
    json_data = request.get_json(force=True)

    userid = json_data["userid"]

    user = get_login(userid)
    if user is None:
        # register fb user with generated password
        password = str(uuid.uuid1()).encode(encoding)
        register_user(userid, password)

    # set session to user
    set_session_id(userid)

    return redirect(url_for('home_bp.home'))