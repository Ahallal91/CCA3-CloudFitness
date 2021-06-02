import boto3
import bcrypt
from flask import Blueprint, render_template, request, flash, session, redirect, url_for

login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

encoding = 'utf-8'

def get_login(email):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('user')
    response = table.get_item(Key={'email': email})

    if 'Item' in response:
        return response['Item']
    else:
        return None

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
        email = get_login(request.form['email'])
        password = request.form['password'].encode(encoding)
        password_valid = validate_password(password, email)
        if password_valid is not None:
            flash(password_valid)
            error = True
        if error:
            return render_template("login.html")
        else:
            flash('Successfully logged in')
            set_session_id(email)
            return redirect(url_for('home_bp.home'))

