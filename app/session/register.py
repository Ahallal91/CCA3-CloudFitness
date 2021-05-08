import json
import boto3
from flask import Blueprint, render_template, request


register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def registerCognito(email, username, password):
    with open('app/config.json') as f:
        data = json.load(f)
    cognito = data.get('cognito')
    client = boto3.client('cognito-idp', region_name=cognito['REGION'])
    response = client.confirm_sign_up(
        ClientId=cognito['USER_POOL_ID'],
        Username=username,
        Email=email,
        Password=password
    )
    return response

@register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        success = registerCognito(email, username, password)
        print(success)