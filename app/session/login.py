import requests
import json
import boto3
import bcrypt
from flask_oauth import OAuth
from flask import Blueprint, render_template, request, flash, session, url_for

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

encoding = 'utf-8'
oauth = OAuth()

with open('app/config.json') as f:
    data = json.load(f)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=data.get('twitter-api')['API_KEY'],
    consumer_secret=data.get('twitter-api')['API_SECRET']
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

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

@login_bp.route("/twitter_login", methods=["GET", "POST"])
def twitter_login():
    return twitter.authorize(callback=url_for('oauth_authorized',
    next=request.args.get('next') or request.referrer or None))
    
@login_bp.route("/login", methods=["GET", "POST"])
def login():
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
            return render_template("login.html")

