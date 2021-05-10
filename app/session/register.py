import json
import boto3
import hmac
import hashlib
import base64
from flask import Blueprint, render_template, request


register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

with open('app/config.json') as f:
    data = json.load(f)
cognito = data.get('cognito')
client = boto3.client('cognito-idp', region_name=cognito['REGION'])
user_pool_id = cognito['USER_POOL_ID']
client_id = cognito['APP_CLIENT_ID']
client_secret = cognito['APP_CLIENT_SECRET']

def secret_hash(username):
    message = username + client_id    
    dig = hmac.new(bytearray(client_secret, "utf-8"), msg=message.encode('UTF-8'),
                    digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def register_cognito(username, email, password):
    response = client.sign_up(
        ClientId=client_id,
        SecretHash=secret_hash(username),
        Username=username,
        Password=password,
        UserAttributes=[ 
            { 
                "Name": "email",
                "Value": email
            },
            {
                "Name": "preferred_username",
                "Value": "email"
            }
        ],
    )
    return response

def confirm_cognito(username, confirm_code):
    response = client.sign_up(
        ClientId=client_id,
        Username=username,
        ConfirmationCode=confirm_code
    )
    return response

@register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        # email = request.form['email']
        # password = request.form['password']
        username1 = 'testuser2'
        email2 = username1
        password1 = "#Abc1234"
        success = register_cognito(email2, username1, password1)
        return render_template("confirm_register.html")

@register_bp.route('/confirm/register', methods=["GET", "POST"])
def confirm_register():
    if request.method == 'GET':
        return render_template("confirm_register.html")
    if request.method == 'POST':
        email = request.form['email']
        code = request.form['confirm']
        success = confirm_cognito(email, code)
        print(success)
        return render_template("confirm_register.html")