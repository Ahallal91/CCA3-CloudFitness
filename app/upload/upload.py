from flask import Blueprint, render_template, session, url_for, request, flash, redirect
import boto3
import logging
import uuid
from botocore.exceptions import ClientError

upload_bp = Blueprint(
    'upload_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

def format_tags(tags):
    return tags.split(',')

def format_image_name(image):
    name = image.filename.split('.')
    name[0] = str(uuid.uuid1())
    image.filename =  f"{name[0]}.{name[1]}"
    return image.filename

def upload_exercise(filename, title, description, level, tags, url, admin_approved):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('exercise')

    id = filename.split('.')

    response = table.put_item(
        Item={
            'id': id[0],
            'title': title,
            'description': description,
            'level': level,
            'tags': tags,
            'url': url,
            'approved': admin_approved
        }
    )

    return response

def upload_exercise_image(file):
    s3_client = boto3.client('s3')
    bucket = 'elasticbeanstalk-ap-southeast-2-059411200951'
    try:
        s3_client.upload_fileobj(file, bucket, f"image_uploads/{file.filename}")
    except ClientError as e:
        logging.error(e)
        return False
    return True

@upload_bp.route('/upload', methods=["GET", "POST"])
def upload():
    session.pop('_flashes', None)
    if session['email'] is None:
        return redirect(url_for('login_bp.login'))
    else:
        exercise_level = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        if request.method == 'GET': 
            return render_template("upload.html", exercise_level=exercise_level)
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            level = request.form['level_select']
            tags = request.form['tags']
            url = request.form['url']
            image = request.files['file']
            image.filename = format_image_name(image)
            tags = format_tags(tags)

            if upload_exercise_image(image):
                upload_exercise(image.filename, title, description, level, tags, url, False)
                flash(f'You have successfully uploaded {title}')
            else:
                flash(f'An error occured uploading the file') 
            return render_template("upload.html", exercise_level=exercise_level)

            