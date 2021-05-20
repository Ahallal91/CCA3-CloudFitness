import bcrypt
import boto3
from flask import Blueprint, render_template, request, redirect, flash, url_for

register_bp = Blueprint(
    'register_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

encoding = 'utf-8'

def validate_user(email, password, password_confirmation):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('user')
    existing_user = table.get_item(Key={'email': email})
    if 'Item' in existing_user:
        return 'User Exists'
    if (password != password_confirmation):
        return 'Passwords must match'

    return None

def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def register_user(email, password):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('user')

    response = table.put_item(
        Item={
            'email': email,
            'password': hash_password(password).decode(encoding)
        }
    )

    return response

@register_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode(encoding)
        password_confirm = request.form['password-confirmation'].encode(encoding)
        validation = validate_user(email, password, password_confirm)
        if validation is not None:
            flash(validation)
            return render_template("register.html")
        else:
            register_user(email, password)
            return redirect(url_for('login_bp.login'))

