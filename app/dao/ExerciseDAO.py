import boto3
import datetime


def format_tags(tags):
    return tags.split(',')


def upload_exercise(title, muscle_group, description, level, tags, image_url, video_url, admin_approved):
    tags = format_tags(tags)
    time = datetime.datetime.now()

    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('exercise')
    response = table.put_item(
        Item={
            'body_part': muscle_group,  # e.g. chest, triceps, biceps, etc
            'name': title,  # name of the exercise, e.g. "squat"
            'description': description,  # user-given description of that exercise
            'level': level,  # difficulty level, e.g. beginner, intermediate, etc.
            'tags': tags,  # user-defined tags
            'video_url': video_url,  # video url
            'image_url': image_url,
            'approved': admin_approved,  # true if an admin has approved the workout, false otherwise
            'upload_date': str(time),  # upload date in the format YYYY-MM-DD HH:MM:SS.MS
            'views': 0,  # number of times exercise has been viewed by all users
            'likes': 0,  # number of likes exercise has received from registered users
        }
    )

    return response
