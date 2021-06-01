from flask import Blueprint, render_template, session, url_for, request, flash, redirect

import app.util as util
import app.dao.ExerciseDAO as ExerciseDAO
import app.dao.StorageDAO as StorageDAO

from app.exceptions.exceptions import ImageUploadFailed
from app.exceptions.exceptions import ExerciseUploadFailed


upload_bp = Blueprint(
    'upload_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@upload_bp.route('/upload', methods=["GET", "POST"])
def upload():
    session.pop('_flashes', None)
    if session['email'] is None:
        return redirect(url_for('login_bp.login'))

    exercise_level = util.get_exercise_levels()
    muscle_groups = util.get_muscle_groups()

    if request.method == 'POST':
        title = request.form['title']
        muscle_group = request.form['muscle_group']
        description = request.form['description']
        level = request.form['level_select']
        tags = request.form['tags']
        video_url = request.form['url']
        image = request.files['file']

        try:
            bucket = "elasticbeanstalk-ap-southeast-2-059411200951"
            image_name = StorageDAO.upload_exercise_image(image, bucket)
            image_url = StorageDAO.get_url_for(bucket, "ap-southeast-2", "image_uploads/", image_name)
            ExerciseDAO.upload_exercise(title, muscle_group, description, level, tags, image_url, video_url, False)
        except (ImageUploadFailed, ExerciseUploadFailed) as e:
            flash(f'{e.message}')
        else:
            flash(f'An unknown error occurred uploading your exercise.')

    return render_template("upload.html", exercise_level=exercise_level, muscle_groups=muscle_groups)
