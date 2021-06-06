from flask import Blueprint, render_template, session, url_for, request, flash, redirect

import app.util as util
from ..dao.ExerciseDAO import ExerciseDAO as ExerciseDAO
from ..dao.ProfilePersonalDAO import ProfilePersonalDAO as ProfilePersonalDAO
from ..dao.StorageDAO import StorageDAO as StorageDAO

from app.exceptions.exceptions import ImageUploadFailed
from app.exceptions.exceptions import ExerciseUploadFailed


upload_bp = Blueprint(
    'upload_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

exerciseDAO = ExerciseDAO()
storageDAO = StorageDAO()
profilePersonalDAO = ProfilePersonalDAO()

def parse_name(string):
    """Keep only characters and spaces, replace spaces with dashes"""
    return ''.join(c for c in string if c.isalpha() or c.isspace()).replace(' ', '-').lower()


@upload_bp.route('/upload', methods=["GET", "POST"])
def upload():
    session.pop('_flashes', None)
    if session['email'] is None:
        return redirect(url_for('login_bp.login'))

    exercise_level = util.get_exercise_levels()
    muscle_groups = util.get_muscle_groups()
    exercise_types = util.get_exercise_types()
    exercise_location = util.get_exercise_upload_type()

    if request.method == 'POST':
        # keep original copies of the exercise type and name for display
        # for the partition and sort keys, since they are used in urls, only keep alphabetical characters and
        # spaces, then replace spaces with dashes and convert  to lowercase
        formatted_exercise_type = request.form['exercise_type']
        partition_exercise_type = parse_name(formatted_exercise_type)
        formatted_name = request.form['name']
        sort_name = parse_name(formatted_name)

        # duplicating sort key as an attribute to make table scannable
        search = sort_name

        # TODO: need to enforce this
        # assuming videos are from youtube, replace the link given with the embed
        video_url = request.form['url']
        video_url = video_url.replace("watch?v=", "embed/")

        # other entries are kept as-is
        level = request.form['level_select']
        muscles = request.form.getlist('muscles')
        description = request.form['description']
        image = request.files['file']
        location = request.form['exercise-location']

        try:
            bucket = "elasticbeanstalk-ap-southeast-2-059411200951"
            image_name = storageDAO.upload_exercise_image(image, bucket)
            image_url = storageDAO.get_url_for(bucket, "ap-southeast-2", "image_uploads/", image_name)
            print(location)
            if location == exercise_location[1]:
                exerciseDAO.upload_exercise(partition_exercise_type, formatted_exercise_type, sort_name, formatted_name,
                                            search, level, muscles, description, video_url, image_url, False)
            elif 'email' in session and location == exercise_location[0]:
                profilePersonalDAO.add_exercise(partition_exercise_type, formatted_exercise_type, sort_name, formatted_name,
                                                search, level, muscle_groups, description, video_url, image_url, session['email'])
            else:
                flash('Please sign in to upload to your profile')
                return render_template("upload.html",
                        exercise_level=exercise_level,
                        muscle_groups=muscle_groups,
                        exercise_types=exercise_types,
                        exercise_location=exercise_location)
            flash(f'Exercise uploaded successfully!')
        except (ImageUploadFailed, ExerciseUploadFailed) as e:
            flash(f'{e.message}')

    return render_template("upload.html",
                           exercise_level=exercise_level,
                           muscle_groups=muscle_groups,
                           exercise_types=exercise_types,
                           exercise_location=exercise_location)
